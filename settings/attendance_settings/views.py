from django.shortcuts import render
from ninja import Router
from .schema import *
from settings.attendance_settings.models import *
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

attendance_settings_api = Router(tags=['attendance_settings'])

@attendance_settings_api.post("/attendance_settings", response={201: Message, 400: Message, 403: Message, 409: Message})
async def create_attendance_settings(request, data: AttendenceSettingSchema):
    created_by = request.auth
    try:
        organization = await sync_to_async(Organization.objects.get)(id=data.organization)
        

        is_authorized = (created_by.role == 'admin') and (created_by.organization_id == organization.id)
        
        if not is_authorized:
            return 403, {"message": "You don't have permission to create settings for this organization"}
    
        exists = await sync_to_async(AttendaceSettings.objects.filter)(organization=organization)
        exists = await sync_to_async(lambda q: q.exists())(exists)
        
        if exists:
            return 409, {"message": "Attendance Settings already exists for this organization"}
        
        settings_data = data.dict()
        settings_data['organization'] = organization  
        settings_data['created_by'] = created_by  
        
        await sync_to_async(AttendaceSettings.objects.create)(**settings_data)
        return 201, {"message": "Attendance Settings created successfully."}
    
    except ObjectDoesNotExist:
        return 400, {"message": "Organization not found"}
    except Exception as e:
        return 400, {"message": str(e)}


@attendance_settings_api.get("/attendance_settings", response={200: AttendenceSettingSchema, 400: Message, 404: Message})
async def get_attendance_settings(request, organization: int):
    try:
        # Fetch the attendance settings using sync_to_async
        attendance_settings = await sync_to_async(AttendaceSettings.objects.get)(organization=organization)

        # Fetch the organization details using sync_to_async
        organization_instance = await sync_to_async(lambda: attendance_settings.organization)()
        organization_schema = organizationDetail(
            id=organization_instance.id,
            name=organization_instance.organization_name
        )

        # Convert the attendance settings to the schema
        attendance_settings_schema = AttendenceSettingSchema(
            organization=organization_schema,
            enable_attendance=attendance_settings.enable_attendance,
            default_attendance_status=attendance_settings.default_attendance_status,
            deduct_salary_for_absent_days=attendance_settings.deduct_salary_for_absent_days,
            company_start_time=attendance_settings.company_start_time,
            company_end_time=attendance_settings.company_end_time,
            hide_total_hours=attendance_settings.hide_total_hours,
            hide_attendance_punches=attendance_settings.hide_attendance_punches,
            disable_web_attendance=attendance_settings.disable_web_attendance,
            enable_ip_restrictions=attendance_settings.enable_ip_restrictions,
            disable_mobile_attendance=attendance_settings.disable_mobile_attendance
        )

        return 200, attendance_settings_schema

    except ObjectDoesNotExist:
        return 404, {"message": "Attendance Settings not found."}
    except Exception as e:
        return 400, {"message": str(e)}


@attendance_settings_api.put("/attendance_settings", response={200: Message, 400: Message, 404: Message})
async def update_attendance_settings(request, data: AttendenceSettingSchema):
    try:
        # Fetch the organization instance using sync_to_async
        organization = await sync_to_async(Organization.objects.get)(id=data.organization.id)

        # Fetch the attendance settings using sync_to_async
        attendance_settings = await sync_to_async(AttendaceSettings.objects.get)(organization=organization)

        # Update the attendance settings
        for key, value in data.dict().items():
            if key != "organization":  # Skip the organization field
                setattr(attendance_settings, key, value)

        # Save the updated attendance settings
        await sync_to_async(attendance_settings.save)()

        return 200, {"message": "Attendance Settings updated successfully."}

    except ObjectDoesNotExist:
        return 404, {"message": "Attendance Settings or Organization not found."}
    except Exception as e:
        return 400, {"message": str(e)}



@attendance_settings_api.post("/roster_shift_settings", response={201: Message, 403: Message, 409: Message})
async def roster_shift_settings(request, data: RosterShiftSettingsSchema):
    created_by = request.auth
    if RosterShiftSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Roster Shift Settings already exists for this organization"}
    RosterShiftSettings.objects.create(**data.dict())
    return 201, {"message": "Roster Shift Settings created successfully."}

@attendance_settings_api.get("/roster_shift_settings", response={200: RosterShiftSettingsSchema, 404: Message})
async def get_roster_shift_settings(request, organization:int):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=organization)
        return 200, roster_shift_settings
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}
    
@attendance_settings_api.put("/roster_shift_settings", response={200: Message, 404: Message})
async def update_roster_shift_settings(request, data: RosterShiftSettingsSchema):
    try:
        roster_shift_settings = RosterShiftSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(roster_shift_settings, key, value)
        roster_shift_settings.save()
        return 200, {"message": "Roster Shift Settings updated successfully."}
    except RosterShiftSettings.DoesNotExist:
        return 404, {"message": "Roster Shift Settings not found."}

   
@attendance_settings_api.post("/shift_change_settings", response={201: Message, 403: Message, 409: Message})
async def shift_change_settings(request, data: ShiftChangeSettingsSchema):
    created_by = request.auth
    if ShiftChangeSettings.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Shift Change Settings already exists for this organization"}
    ShiftChangeSettings.objects.create(**data.dict())
    return 201, {"message": "Shift Change Settings created successfully."}

@attendance_settings_api.get("/shift_change_settings", response={200: ShiftChangeSettingsSchema, 404: Message})
async def get_shift_change_settings(request, organization:int):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=organization)
        return 200, shift_change_settings
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."}
    
@attendance_settings_api.put("/shift_change_settings", response={200: Message, 404: Message})
async def update_shift_change_settings(request, data: ShiftChangeSettingsSchema):
    try:
        shift_change_settings = ShiftChangeSettings.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(shift_change_settings, key, value)
        shift_change_settings.save()
        return 200, {"message": "Shift Change Settings updated successfully."}
    except ShiftChangeSettings.DoesNotExist:
        return 404, {"message": "Shift Change Settings not found."} 
    
@attendance_settings_api.post("/regularization_policies", response={201: Message, 403: Message, 409: Message})
async def regularization_policies(request, data: RegularizationPoliciesSchema):
    created_by = request.auth
    if RegularizationPolicies.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Regularization Policies already exists for this organization"}
    RegularizationPolicies.objects.create(**data.dict())
    return 201, {"message": "Regularization Policies created successfully."}

@attendance_settings_api.get("/regularization_policies", response={200: RegularizationPoliciesSchema, 404: Message})
async def get_regularization_policies(request, organization:int):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=organization)
        return 200, regularization_policies
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
@attendance_settings_api.put("/regularization_policies", response={200: Message, 404: Message})
async def update_regularization_policies(request, data: RegularizationPoliciesSchema):
    try:
        regularization_policies = RegularizationPolicies.objects.get(organization=data.organization)
        for key, value in data.dict().items():
            setattr(regularization_policies, key, value)
        regularization_policies.save()
        return 200, {"message": "Regularization Policies updated successfully."}
    except RegularizationPolicies.DoesNotExist:
        return 404, {"message": "Regularization Policies not found."}
    
@attendance_settings_api.post("/sandwich_rules", response={201: Message, 400: Message, 403: Message, 409: Message})
async def create_sandwich_rules(request, data: SandwichRulesSettingsSchema):
    created_by = request.auth
    try:
        # Get organization instance
        organization = await sync_to_async(Organization.objects.get)(id=data.organization)
        
        # Check if the user is an admin and belongs to the same organization
        is_authorized = (created_by.role == 'admin') and (created_by.organization_id == organization.id)
        
        if not is_authorized:
            return 403, {"message": "You don't have permission to create sandwich rules for this organization"}
        
        # Check if rules already exist for this organization
        exists = await sync_to_async(SandwichRulesSettings.objects.filter)(organization=organization)
        exists = await sync_to_async(lambda q: q.exists())(exists)
        
        if exists:
            return 409, {"message": "Sandwich Rules already exist for this organization"}
        
        # Create settings data
        settings_data = {
            'organization': organization,
            'created_by': created_by,
            'enable_sandwich_rules': data.enable_sandwich_rules,
            'week_off_holidays_between_absents': data.week_off_holidays_between_absents,
            'week_off_holidays_after_absent': data.week_off_holidays_after_absent,
            'week_off_holidays_before_absent': data.week_off_holidays_before_absent,
            'absent_week_offs_holidays_beginning_month': data.absent_week_offs_holidays_beginning_month,
            'absent_week_offs_holidays_end_month': data.absent_week_offs_holidays_end_month
        }
        
        # Create sandwich rules
        await sync_to_async(SandwichRulesSettings.objects.create)(**settings_data)
        return 201, {"message": "Sandwich Rules created successfully"}
    
    except Organization.DoesNotExist:
        return 400, {"message": "Organization not found"}
    except Exception as e:
        return 400, {"message": str(e)}


@attendance_settings_api.get("/sandwich_rules/{organization_id}", response={200: SandwichRulesSettingsSchema, 404: Message})
async def get_sandwich_rules(request, organization_id: int):
    try:
        # Get organization
        organization = await sync_to_async(Organization.objects.get)(id=organization_id)
        
        # Get sandwich rules
        sandwich_rules = await sync_to_async(SandwichRulesSettings.objects.get)(organization=organization)
        
        # Convert to schema
        result = SandwichRulesSettingsSchema(
            organization=organization_id,
            enable_sandwich_rules=sandwich_rules.enable_sandwich_rules,
            week_off_holidays_between_absents=sandwich_rules.week_off_holidays_between_absents,
            week_off_holidays_after_absent=sandwich_rules.week_off_holidays_after_absent,
            week_off_holidays_before_absent=sandwich_rules.week_off_holidays_before_absent,
            absent_week_offs_holidays_beginning_month=sandwich_rules.absent_week_offs_holidays_beginning_month,
            absent_week_offs_holidays_end_month=sandwich_rules.absent_week_offs_holidays_end_month
        )
        
        return 200, result
    
    except Organization.DoesNotExist:
        return 404, {"message": "Organization not found"}
    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules not found for this organization"}
    except Exception as e:
        return 400, {"message": str(e)}


@attendance_settings_api.put("/sandwich_rules/{organization_id}", response={200: Message, 403: Message, 404: Message})
async def update_sandwich_rules(request, organization_id: int, data: SandwichRulesSettingsSchema):
    created_by = request.auth
    try:
        # Get organization
        organization = await sync_to_async(Organization.objects.get)(id=organization_id)
        
        # Check if the user is an admin and belongs to the same organization
        is_authorized = (created_by.role == 'admin') and (created_by.organization_id == organization.id)
        
        if not is_authorized:
            return 403, {"message": "You don't have permission to update sandwich rules for this organization"}
        
        # Get sandwich rules
        sandwich_rules = await sync_to_async(SandwichRulesSettings.objects.get)(organization=organization)
        
        # Update fields
        sandwich_rules.enable_sandwich_rules = data.enable_sandwich_rules
        sandwich_rules.week_off_holidays_between_absents = data.week_off_holidays_between_absents
        sandwich_rules.week_off_holidays_after_absent = data.week_off_holidays_after_absent
        sandwich_rules.week_off_holidays_before_absent = data.week_off_holidays_before_absent
        sandwich_rules.absent_week_offs_holidays_beginning_month = data.absent_week_offs_holidays_beginning_month
        sandwich_rules.absent_week_offs_holidays_end_month = data.absent_week_offs_holidays_end_month
        sandwich_rules.updated_by = created_by
        
        # Save changes
        await sync_to_async(sandwich_rules.save)()
        
        return 200, {"message": "Sandwich Rules updated successfully"}
    
    except Organization.DoesNotExist:
        return 404, {"message": "Organization not found"}
    except SandwichRulesSettings.DoesNotExist:
        return 404, {"message": "Sandwich Rules not found for this organization"}
    except Exception as e:
        return 400, {"message": str(e)}
# Overtime Compensation and CompOff Settings

# Overtime Settings
@attendance_settings_api.post("/overtime_settings", response={201: dict, 409: dict})
def create_overtime_settings(request, data: OvertimeSettingsSchema):
    if TimeManagementPolicy.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Overtime Settings already exist for this organization."}
    
    TimeManagementPolicy.objects.create(**data.dict())
    return 201, {"message": "Overtime Settings created successfully."}

@attendance_settings_api.get("/overtime_settings/{organization_id}", response={200: OvertimeSettingsSchema, 404: dict})
def get_overtime_settings(request, organization_id: int):
    try:
        overtime_settings = TimeManagementPolicy.objects.get(organization=organization_id)
        return 200, overtime_settings
    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Overtime Settings not found for this organization."}

@attendance_settings_api.put("/overtime_settings/{organization_id}", response={200: dict, 404: dict})
def update_overtime_settings(request, organization_id: int, data: OvertimeSettingsSchema):
    try:
        overtime_settings = TimeManagementPolicy.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(overtime_settings, key, value)
        overtime_settings.save()
        return 200, {"message": "Overtime Settings updated successfully."}
    except TimeManagementPolicy.DoesNotExist:
        return 404, {"message": "Overtime Settings not found for this organization."}

# Compensation Rules
@attendance_settings_api.post("/compensation_rules", response={201: dict, 409: dict})
def create_compensation_rules(request, data: CompensationRulesSchema):
    if CompensationRules.objects.filter(organization=data.organization).exists():
        return 409, {"message": "Compensation Rules already exist for this organization."}
    
    CompensationRules.objects.create(**data.dict())
    return 201, {"message": "Compensation Rules created successfully."}

@attendance_settings_api.get("/compensation_rules/{organization_id}", response={200: CompensationRulesSchema, 404: dict})
def get_compensation_rules(request, organization_id: int):
    try:
        compensation_rules = CompensationRules.objects.get(organization=organization_id)
        return 200, compensation_rules
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found for this organization."}

@attendance_settings_api.put("/compensation_rules/{organization_id}", response={200: dict, 404: dict})
def update_compensation_rules(request, organization_id: int, data: CompensationRulesSchema):
    try:
        compensation_rules = CompensationRules.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(compensation_rules, key, value)
        compensation_rules.save()
        return 200, {"message": "Compensation Rules updated successfully."}
    except CompensationRules.DoesNotExist:
        return 404, {"message": "Compensation Rules not found for this organization."}

# CompOff Rules
@attendance_settings_api.post("/compoff_rules", response={201: dict, 409: dict})
def create_compoff_rules(request, data: CompOffRulesSchema):
    if CompOffRules.objects.filter(organization=data.organization).exists():
        return 409, {"message": "CompOff Rules already exist for this organization."}
    
    CompOffRules.objects.create(**data.dict())
    return 201, {"message": "CompOff Rules created successfully."}

@attendance_settings_api.get("/compoff_rules/{organization_id}", response={200: CompOffRulesSchema, 404: dict})
def get_compoff_rules(request, organization_id: int):
    try:
        compoff_rules = CompOffRules.objects.get(organization=organization_id)
        return 200, compoff_rules
    except CompOffRules.DoesNotExist:
        return 404, {"message": "CompOff Rules not found for this organization."}

@attendance_settings_api.put("/compoff_rules/{organization_id}", response={200: dict, 404: dict})
def update_compoff_rules(request, organization_id: int, data: CompOffRulesSchema):
    try:
        compoff_rules = CompOffRules.objects.get(organization=organization_id)
        for key, value in data.dict().items():
            setattr(compoff_rules, key, value)
        compoff_rules.save()
        return 200, {"message": "CompOff Rules updated successfully."}
    except CompOffRules.DoesNotExist:
        return 404, {"message": "CompOff Rules not found for this organization."}
    
# Undertime Rules

@attendance_settings_api.post("/undertime_rules", response={201: UnderTimeRuleSchema, 400: Message, 409: Message})
async def create_undertime_rule(request, data: UnderTimeRuleSchema):
    user = request.auth  
    if user and await sync_to_async(lambda: user.role == 'admin' and user.organization)():
        try:
            organization = await sync_to_async(Organization.objects.get)(id=data.organization)
            exists = await sync_to_async(UnderTimeRule.objects.filter(organization=organization).exists)()
            if exists:
                return 409, {"message": "Undertime rules already exist for this organization"}

            undertime_rule = await sync_to_async(UnderTimeRule.objects.create)(
                organization=organization,
                created_by=user,
                eligiblity_hours=data.eligiblity_hours,
                consider_absent=data.consider_absent,
                conside_half_day=data.conside_half_day
            )

            return 201, UnderTimeRuleSchema.from_orm(undertime_rule)

        except ObjectDoesNotExist:
            return 400, {"message": "Organization not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    return 400, {"message": "Unauthorized access"}


@attendance_settings_api.get("/undertime_rules/{organization_id}", response={200: UnderTimeRuleSchema, 404: Message})
async def get_undertime_rules(request, organization_id: int):
    try:
        undertime_rule = await sync_to_async(UnderTimeRule.objects.get)(organization=organization_id)
        return 200, UnderTimeRuleSchema.from_orm(undertime_rule)
    except UnderTimeRule.DoesNotExist:
        return 404, {"message": "Undertime rules not found for this organization"}
    
@attendance_settings_api.put("/undertime_rules/{organization_id}", response={200: UnderTimeRuleSchema, 404: Message})
async def update_undertime_rules(request, organization_id: int, data: UnderTimeRuleSchema):
    try:
        undertime_rule = await sync_to_async(UnderTimeRule.objects.get)(organization=organization_id)
        for key, value in data.dict().items():
            setattr(undertime_rule, key, value)
        await sync_to_async(undertime_rule.save)()
        return 200, UnderTimeRuleSchema.from_orm(undertime_rule)
    except UnderTimeRule.DoesNotExist:
        return 404, {"message": "Undertime rules not found for this organization"}
    
@attendance_settings_api.delete("/undertime_rules/{organization_id}", response={200: Message, 404: Message})
async def delete_undertime_rules(request, organization_id: int):
    try:
        undertime_rule = await sync_to_async(UnderTimeRule.objects.get)(organization=organization_id)
        await sync_to_async(undertime_rule.delete)()
        return 200, {"message": "Undertime rules deleted successfully"}
    except UnderTimeRule.DoesNotExist:
        return 404, {"message": "Undertime rules not found for this organization"}