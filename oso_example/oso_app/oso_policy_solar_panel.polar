allow(actor: ElectronicDevice, "plug_in", resource: SolarPanel) if
    resource.provided_power >= resource.get_used_work_power() + actor.work_power;

actor ElectronicDevice {}

resource SolarPanel {}
