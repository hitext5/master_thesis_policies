package main

import (
    "github.com/hashicorp/sentinel-sdk"
    "github.com/hashicorp/sentinel-sdk/framework"
)

type SmartPlug struct {
    RatedPower int
    Slots      int
}

func main() {
    sdk.NewPlugin("plug",
        func() interface{} {
            return &SmartPlug{
                RatedPower: 1000,
                Slots:      4,
            }
        },
        func(m *framework.PluginMap) error {
            m.Map("rated_power", func(args ...interface{}) (interface{}, error) {
                sp := args[0].(*SmartPlug)
                return sp.RatedPower, nil
            })
            m.Map("slots", func(args ...interface{}) (interface{}, error) {
                sp := args[0].(*SmartPlug)
                return sp.Slots, nil
            })
            return nil
        },
    )
}