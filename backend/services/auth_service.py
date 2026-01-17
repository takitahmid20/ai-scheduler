"""
Authentication Service
Business logic for user authentication and authorization
"""

from typing import Optional, Dict, Any
import bcrypt
from sqlalchemy.orm import Session

from ..models.user import User
from ..database import SessionLocal

class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against hashed password"""
        # Convert strings to bytes for bcrypt
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password using bcrypt"""
        # Truncate password to 72 bytes (bcrypt limitation)
        password_bytes = password.encode('utf-8')[:72]
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Return as string for database storage
        return hashed.decode('utf-8')
    
    @staticmethod
    def signup(email: str, password: str, full_name: str, 
              student_id: Optional[str] = None, 
              department: Optional[str] = None) -> Dict[str, Any]:
        """
        Register a new user
        Returns: Dict with success status and data or error message
        """
        db = SessionLocal()
        try:
            # Validate input
            if len(password) < 6:
                return {"success": False, "error": "Password must be at least 6 characters"}
            
            # Check if user exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return {"success": False, "error": "Email already registered"}
            
            if student_id:
                existing_student = db.query(User).filter(User.student_id == student_id).first()
                if existing_student:
                    return {"success": False, "error": "Student ID already registered"}
            
            # Create new user
            hashed_password = AuthService.get_password_hash(password)
            new_user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                student_id=student_id,
                department=department,
                is_active=True,
                is_admin=False
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return {
                "success": True,
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "full_name": new_user.full_name,
                    "student_id": new_user.student_id,
                    "department": new_user.department
                }
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()
    
    @staticmethod
    def signin(email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user
        Returns: Dict with success status and user data or error message
        """
        db = SessionLocal()
        try:
            # Find user
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return {"success": False, "error": "Invalid email or password"}
            
            # Verify password
            if not AuthService.verify_password(password, user.hashed_password):
                return {"success": False, "error": "Invalid email or password"}
            
            if not user.is_active:
                return {"success": False, "error": "Account is inactive"}
            
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "student_id": user.student_id,
                    "department": user.department,
                    "is_admin": user.is_admin
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            db.close()
    
    @staticmethod
    def admin_signin(email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate admin user
        Returns: Dict with success status and admin data or error message
        """
        from ..config import ADMIN_EMAIL, ADMIN_PASSWORD
        
        # Check hardcoded admin credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            return {
                "success": True,
                "user": {
                    "email": email,
                    "full_name": "Admin",
                    "is_admin": True
                }
            }
        
        # Also check database for admin users
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email, User.is_admin == True).first()
            if user and AuthService.verify_password(password, user.hashed_password):
                return {
                    "success": True,
                    "user": {
                        "email": user.email,
                        "full_name": user.full_name,
                        "is_admin": True
                    }
                }
            return {"success": False, "error": "Invalid admin credentials"}
        finally:
            db.close()
