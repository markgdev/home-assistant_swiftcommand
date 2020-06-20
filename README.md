# Swift Command Caravan Monitor

## Installation
### Copy component to custom_components directory
```
cp custom_components/swiftcommand /path/to/config/custom_components/
```

### Get your caravan's asset id from the swift command webpage url.
Navigate to the remote access page on the swift command webpage in your browser. The assetid is the number at the end of the URL in the address bar.

![Asset ID](https://github.com/markgdev/home-assistant_swiftcommand/raw/master/images/assetid.png)


### configuration.yaml entry
```yaml
sensor:
- platform: "swiftcommand"
  email: "my@email.com"
  password: "mysupersecretpassword"
  assetid: 12345 # See above screenshot on how to find this
```

## Entity
An entity namaed sensor.swiftcommand will be created with a state of the vehicle voltage and extra information including location, temperature and van details in the attributes.

## Example panel

```yaml
cards:
  - dark_mode: false
    default_zoom: 12
    entities:
      - entity: sensor.swiftcommand
    hours_to_show: 12
    title: Caravan
    type: map
  - entity: sensor.swiftcommand
    filter:
      include:
        - key: sensor.swiftcommand.make
          name: Make
        - key: sensor.swiftcommand.model
          name: Model
        - key: sensor.swiftcommand.temp
          name: Temperature
        - key: sensor.swiftcommand.voltage
          name: Voltage
        - key: sensor.swiftcommand.van_serial
          name: Serial
        - key: sensor.swiftcommand.time
          name: Last Update
        - key: sensor.swiftcommand.latitude
          name: Lat
        - key: sensor.swiftcommand.longitude
          name: Long
    heading_name: Name
    heading_state: Value
    type: 'custom:entity-attributes-card'
type: horizontal-stack

```

![Example panel](https://github.com/markgdev/home-assistant_swiftcommand/raw/master/images/mapexample.png)