"""
MongoDB database handler for HR Management System.
Provides connection management and database operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError, ConnectionFailure
from config import config

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handles all MongoDB database operations."""
    
    def __init__(self):
        """Initialize database connection."""
        self.client: Optional[MongoClient] = None
        self.db = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(
                config.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[config.MONGODB_DB_NAME]
            self._create_indexes()
            logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self) -> None:
        """Create necessary indexes for performance."""
        try:
            # Users collection indexes
            self.db.users.create_index([("email", ASCENDING)], unique=True)
            self.db.users.create_index([("role", ASCENDING)])
            self.db.users.create_index([("organization", ASCENDING)])
            self.db.users.create_index([("isDeleted", ASCENDING)])
            
            # Attendances collection indexes
            self.db.attendances.create_index([("userId", ASCENDING)])
            self.db.attendances.create_index([("date", DESCENDING)])
            self.db.attendances.create_index([("status", ASCENDING)])
            self.db.attendances.create_index([
                ("userId", ASCENDING),
                ("date", DESCENDING)
            ])
            
            logger.info("Database indexes created successfully")
        except PyMongoError as e:
            logger.warning(f"Error creating indexes: {e}")
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        try:
            if not ObjectId.is_valid(user_id):
                return None
            return self.db.users.find_one({"_id": ObjectId(user_id), "isDeleted": {"$ne": True}})
        except PyMongoError as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        try:
            return self.db.users.find_one({"email": email, "isDeleted": {"$ne": True}})
        except PyMongoError as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def search_users(self, query: Dict) -> List[Dict]:
        """Search users with custom query."""
        try:
            # Add isDeleted filter
            query["isDeleted"] = {"$ne": True}
            return list(self.db.users.find(query))
        except PyMongoError as e:
            logger.error(f"Error searching users: {e}")
            return []
    
    def get_attendance_by_user_and_date(
        self, user_id: str, date: datetime
    ) -> Optional[Dict]:
        """Get attendance record for a user on a specific date."""
        try:
            if not ObjectId.is_valid(user_id):
                return None
            
            # Set date to start of day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            return self.db.attendances.find_one({
                "userId": ObjectId(user_id),
                "date": {"$gte": start_of_day, "$lte": end_of_day}
            })
        except PyMongoError as e:
            logger.error(f"Error getting attendance: {e}")
            return None
    
    def get_user_attendances(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Get attendance records for a user within date range."""
        try:
            if not ObjectId.is_valid(user_id):
                return []
            
            query = {"userId": ObjectId(user_id)}
            
            if start_date or end_date:
                date_query = {}
                if start_date:
                    date_query["$gte"] = start_date
                if end_date:
                    date_query["$lte"] = end_date
                query["date"] = date_query
            
            return list(
                self.db.attendances.find(query).sort("date", DESCENDING)
            )
        except PyMongoError as e:
            logger.error(f"Error getting user attendances: {e}")
            return []
    
    def create_attendance(self, attendance_data: Dict) -> Optional[str]:
        """Create a new attendance record."""
        try:
            result = self.db.attendances.insert_one(attendance_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error creating attendance: {e}")
            return None
    
    def update_attendance(self, attendance_id: str, update_data: Dict) -> bool:
        """Update an attendance record."""
        try:
            if not ObjectId.is_valid(attendance_id):
                return False
            
            result = self.db.attendances.update_one(
                {"_id": ObjectId(attendance_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"Error updating attendance: {e}")
            return False
    
    def get_attendance_statistics(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get attendance statistics with optional filters."""
        try:
            match_stage = {}
            
            if user_id and ObjectId.is_valid(user_id):
                match_stage["userId"] = ObjectId(user_id)
            
            if start_date or end_date:
                date_query = {}
                if start_date:
                    date_query["$gte"] = start_date
                if end_date:
                    date_query["$lte"] = end_date
                match_stage["date"] = date_query
            
            if status:
                match_stage["status"] = status
            
            pipeline = [
                {"$match": match_stage},
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1},
                        "total_hours": {"$sum": "$totalWorkingHours"}
                    }
                }
            ]
            
            results = list(self.db.attendances.aggregate(pipeline))
            
            stats = {
                "total_records": sum(r["count"] for r in results),
                "by_status": {r["_id"]: r["count"] for r in results},
                "total_working_hours": sum(
                    r.get("total_hours", 0) for r in results if r.get("total_hours")
                )
            }
            
            return stats
        except PyMongoError as e:
            logger.error(f"Error getting attendance statistics: {e}")
            return {}
    
    def get_users_by_department(self, designation: str) -> List[Dict]:
        """Get all users in a specific department/designation."""
        try:
            return list(self.db.users.find({
                "designation": designation,
                "isDeleted": {"$ne": True}
            }))
        except PyMongoError as e:
            logger.error(f"Error getting users by department: {e}")
            return []
    
    def aggregate_query(self, collection: str, pipeline: List[Dict]) -> List[Dict]:
        """Execute custom aggregation pipeline."""
        try:
            return list(self.db[collection].aggregate(pipeline))
        except PyMongoError as e:
            logger.error(f"Error executing aggregation: {e}")
            return []
    
    def close(self) -> None:
        """Close database connection."""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")


# Global database instance
db_handler = DatabaseHandler()