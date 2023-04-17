include("oso_policy_open_door_and_window.polar");

allow(actor: LocationAndTime, "turn_on", resource: LightAndDoor) if
    allow(actor, "lock", resource) and
    resource.light_bulb.turned_on == false and
    after_sunset(actor) or before_sunrise(actor);

after_sunset(actor: LocationAndTime) if
    actor.clock.current_time > 18;

before_sunrise(actor: LocationAndTime) if
    actor.clock.current_time < 6;

actor LocationAndTime {}

resource LightBulb {}
