#!/usr/bin/env python3

import asyncio
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import aiohttp
import base64
from urllib.parse import urlencode
from dotenv import load_dotenv
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Tool,
)
import mcp.types as types

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("athena-health-mcp")

class AthenaHealthMCP:
    def __init__(self):
        self.server = Server("athena-health-scheduling")
        
        # Configuration from environment variables
        self.base_url = os.getenv("ATHENA_BASE_URL", "https://api.athenahealth.com")
        self.client_id = os.getenv("ATHENA_CLIENT_ID", "")
        self.client_secret = os.getenv("ATHENA_CLIENT_SECRET", "")
        self.practice_id = os.getenv("ATHENA_PRACTICE_ID", "")
        
        # Authentication state
        self.access_token = None
        self.token_expiry = None
        
        if not all([self.client_id, self.client_secret, self.practice_id]):
            logger.error("Missing required environment variables: ATHENA_CLIENT_ID, ATHENA_CLIENT_SECRET, ATHENA_PRACTICE_ID")
        
        self.setup_handlers()

    async def authenticate(self) -> str:
        """Authenticate with Athena Health API and return access token"""
        # Check if token is still valid
        if (self.access_token and self.token_expiry and 
            datetime.now() < self.token_expiry):
            return self.access_token

        auth_string = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "athena/service/Athenanet.MDP.*"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/oauth2/v1/token",
                    headers=headers,
                    data=urlencode(data)
                ) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data["access_token"]
                        # Set expiry with 1 minute buffer
                        expires_in = token_data.get("expires_in", 3600)
                        self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 60)
                        return self.access_token
                    else:
                        error_text = await response.text()
                        raise Exception(f"Authentication failed: {response.status} - {error_text}")
            
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                raise

    async def make_api_request(
        self, 
        endpoint: str, 
        method: str = "GET", 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make authenticated API request to Athena Health"""
        token = await self.authenticate()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/v1/{self.practice_id}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    json=data,
                    params=params
                ) as response:
                    if response.status in [200, 201]:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"API request failed: {response.status} - {error_text}")
                        raise Exception(f"API request failed: {response.status} - {error_text}")
                        
            except Exception as e:
                logger.error(f"API request error: {e}")
                raise

    def setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="get_appointments",
                    description="Get appointments for a specific date range and optional provider",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format"
                            },
                            "end_date": {
                                "type": "string", 
                                "description": "End date in YYYY-MM-DD format"
                            },
                            "provider_id": {
                                "type": "string",
                                "description": "Optional provider ID to filter appointments"
                            },
                            "department_id": {
                                "type": "string",
                                "description": "Optional department ID to filter appointments"
                            }
                        },
                        "required": ["start_date", "end_date"]
                    }
                ),
                Tool(
                    name="get_available_slots",
                    description="Get available appointment slots for scheduling",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "department_id": {
                                "type": "string",
                                "description": "Department ID"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format"
                            }
                        },
                        "required": ["department_id", "start_date", "end_date"]
                    }
                ),
                Tool(
                    name="create_appointment",
                    description="Create a new appointment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "patient_id": {
                                "type": "string",
                                "description": "Patient ID"
                            },
                            "provider_id": {
                                "type": "string",
                                "description": "Provider ID"
                            },
                            "department_id": {
                                "type": "string",
                                "description": "Department ID"
                            },
                            "appointment_type_id": {
                                "type": "string",
                                "description": "Appointment type ID"
                            },
                            "appointment_date": {
                                "type": "string",
                                "description": "Appointment date in YYYY-MM-DD format"
                            },
                            "appointment_time": {
                                "type": "string",
                                "description": "Appointment time in HH:MM format"
                            },
                            "reason_for_visit": {
                                "type": "string",
                                "description": "Reason for the visit"
                            }
                        },
                        "required": ["patient_id", "provider_id", "department_id", "appointment_type_id", "appointment_date", "appointment_time"]
                    }
                ),
                Tool(
                    name="update_appointment",
                    description="Update an existing appointment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "string",
                                "description": "Appointment ID to update"
                            },
                            "appointment_date": {
                                "type": "string",
                                "description": "New appointment date in YYYY-MM-DD format"
                            },
                            "appointment_time": {
                                "type": "string",
                                "description": "New appointment time in HH:MM format"
                            },
                            "reason_for_visit": {
                                "type": "string",
                                "description": "Updated reason for the visit"
                            },
                            "notes": {
                                "type": "string",
                                "description": "Additional notes"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                ),
                Tool(
                    name="cancel_appointment",
                    description="Cancel an appointment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "string",
                                "description": "Appointment ID to cancel"
                            },
                            "cancellation_reason": {
                                "type": "string",
                                "description": "Reason for cancellation"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                ),
                Tool(
                    name="get_providers",
                    description="Get list of providers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "department_id": {
                                "type": "string",
                                "description": "Optional department ID to filter providers"
                            },
                            "specialty": {
                                "type": "string",
                                "description": "Optional specialty to filter providers"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_departments",
                    description="Get list of departments",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_appointment_types",
                    description="Get available appointment types",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "department_id": {
                                "type": "string",
                                "description": "Optional department ID to filter appointment types"
                            },
                            "provider_id": {
                                "type": "string",
                                "description": "Optional provider ID to filter appointment types"
                            }
                        }
                    }
                ),
                Tool(
                    name="search_patients",
                    description="Search for patients by name, DOB, or phone",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "first_name": {
                                "type": "string",
                                "description": "Patient first name"
                            },
                            "last_name": {
                                "type": "string",
                                "description": "Patient last name"
                            },
                            "date_of_birth": {
                                "type": "string",
                                "description": "Date of birth in YYYY-MM-DD format"
                            },
                            "phone": {
                                "type": "string",
                                "description": "Phone number"
                            },
                            "email": {
                                "type": "string",
                                "description": "Email address"
                            }
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool calls"""
            try:
                if name == "get_appointments":
                    result = await self.get_appointments(arguments)
                elif name == "get_available_slots":
                    result = await self.get_available_slots(arguments)
                elif name == "create_appointment":
                    result = await self.create_appointment(arguments)
                elif name == "update_appointment":
                    result = await self.update_appointment(arguments)
                elif name == "cancel_appointment":
                    result = await self.cancel_appointment(arguments)
                elif name == "get_providers":
                    result = await self.get_providers(arguments)
                elif name == "get_departments":
                    result = await self.get_departments(arguments)
                elif name == "get_appointment_types":
                    result = await self.get_appointment_types(arguments)
                elif name == "search_patients":
                    result = await self.search_patients(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
                
            except Exception as e:
                logger.error(f"Tool call error: {e}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    # Tool implementation methods
    async def get_appointments(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get appointments for date range"""
        params = {
            "startdate": args["start_date"],
            "enddate": args["end_date"]
        }
        
        if "provider_id" in args:
            params["providerid"] = args["provider_id"]
        if "department_id" in args:
            params["departmentid"] = args["department_id"]
            
        return await self.make_api_request("/appointments", params=params)

    async def get_available_slots(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get available appointment slots"""
        params = {
            "departmentid": args["department_id"],
            # "appointmenttypeid": args["appointment_type_id"],
            "startdate": args["start_date"],
            "enddate": args["end_date"],
            "reasonid": -1
        }
        
        return await self.make_api_request("/appointments/open", params=params)

    async def create_appointment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new appointment"""
        data = {
            "patientid": args["patient_id"],
            "providerid": args["provider_id"],
            "departmentid": args["department_id"],
            "appointmenttypeid": args["appointment_type_id"],
            "appointmentdate": args["appointment_date"],
            "appointmenttime": args["appointment_time"]
        }
        
        if "reason_for_visit" in args:
            data["reasonforvisit"] = args["reason_for_visit"]
            
        return await self.make_api_request("/appointments", method="POST", data=data)

    async def update_appointment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing appointment"""
        appointment_id = args["appointment_id"]
        data = {}
        
        if "appointment_date" in args:
            data["appointmentdate"] = args["appointment_date"]
        if "appointment_time" in args:
            data["appointmenttime"] = args["appointment_time"]
        if "reason_for_visit" in args:
            data["reasonforvisit"] = args["reason_for_visit"]
        if "notes" in args:
            data["notes"] = args["notes"]
            
        return await self.make_api_request(f"/appointments/{appointment_id}", method="PUT", data=data)

    async def cancel_appointment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel an appointment"""
        appointment_id = args["appointment_id"]
        data = {"appointmentstatus": "x"}  # 'x' typically means cancelled
        
        if "cancellation_reason" in args:
            data["cancellationreason"] = args["cancellation_reason"]
            
        return await self.make_api_request(f"/appointments/{appointment_id}", method="PUT", data=data)

    async def get_providers(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get list of providers"""
        params = {}
        
        if "department_id" in args:
            params["departmentid"] = args["department_id"]
        if "specialty" in args:
            params["specialty"] = args["specialty"]
            
        return await self.make_api_request("/providers", params=params)

    async def get_departments(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get list of departments"""
        return await self.make_api_request("/departments")

    async def get_appointment_types(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get appointment types"""
        params = {}
        
        if "department_id" in args:
            params["departmentid"] = args["department_id"]
        if "provider_id" in args:
            params["providerid"] = args["provider_id"]
            
        return await self.make_api_request("/appointmenttypes", params=params)

    async def search_patients(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for patients"""
        params = {}
        
        if "first_name" in args:
            params["firstname"] = args["first_name"]
        if "last_name" in args:
            params["lastname"] = args["last_name"]
        if "date_of_birth" in args:
            params["dob"] = args["date_of_birth"]
        if "phone" in args:
            params["homephone"] = args["phone"]
        if "email" in args:
            params["email"] = args["email"]
            
        return await self.make_api_request("/patients", params=params)

async def main():
    """Main function to run the MCP server"""
    mcp = AthenaHealthMCP()
    
    # Run the server using stdin/stdout streams
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="athena-health-scheduling",
                server_version="0.1.0",
                capabilities=mcp.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    # Required environment variables check
    required_vars = ["ATHENA_CLIENT_ID", "ATHENA_CLIENT_SECRET", "ATHENA_PRACTICE_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("export ATHENA_CLIENT_ID='your_client_id'")
        print("export ATHENA_CLIENT_SECRET='your_client_secret'")
        print("export ATHENA_PRACTICE_ID='your_practice_id'")
        print("export ATHENA_BASE_URL='https://api.athenahealth.com'  # Optional, defaults to production")
        exit(1)
    
    asyncio.run(main())