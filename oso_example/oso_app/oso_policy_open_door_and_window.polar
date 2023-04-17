allow(actor: SmokeDetector, "unlock", resource: Door) if
    actor.smoke_detected == true and resource.locked == true;

allow(actor: ApartmentOwner, "lock", resource: Door) if
    actor.at_home == false and resource.locked == false;

allow(actor: LocationAndTime, "lock", resource: LightAndDoor) if
    actor.apartment_owner.at_home == false and resource.door.locked == false;

actor SmokeDetector {}

actor ApartmentOwner {}

resource Door {}

# For Polar to work, resource needs to be utilized in the policy.

# In rego the hierarchy is relevant and used to determine the order of evaluation.
# In Polar, the order of evaluation is irrelevant
# because the policy is evaluated by the provided actor and resource, which means that there can be no conflict.