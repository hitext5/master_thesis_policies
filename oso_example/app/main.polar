allow(actor: ElectronicDevice, "plug_in", resource: SmartPlug) if
  has_power(actor, resource) and
  resource.slots >= 1;

actor ElectronicDevice {}

resource SmartPlug {}

has_power(actor: ElectronicDevice, resource: SmartPlug) if
  actor.work_power <= resource.rated_power;
