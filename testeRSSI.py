from rssi import RSSI_Localizer

accessPoints = [{
        'signalAttenuation': 3, 
        'location': {
            'y': 1, 
            'x': 1
        }, 
        'reference': {
            'distance': 4, 
            'signal': -50
        }, 
        'name': 'node1'
    },
    {
        'signalAttenuation': 4, 
        'location': {
            'y': 1, 
            'x': 7
        }, 
        'reference': {
            'distance': 3, 
            'signal': -41
        }, 
        'name': 'node2'
     },{
        'signalAttenuation': 3, 
        'location': {
            'y': 2, 
            'x': 9
        }, 
        'reference': {
            'distance': 5, 
            'signal': -80
        }, 
        'name': 'node3'
     }]
#signalStrength = -69
rssi_localizer_instance = RSSI_Localizer(accessPoints)
#distance = rssi_localizer_instance.getDistanceFromAP(accessPoint, signalStrength)
distance = rssi_localizer_instance.getDistancesForAllAPs([-80,-70,-50,-80,-80,-80])
position = rssi_localizer_instance.getNodePosition([-80,-70,-50,-80,-80,-80])

print(position)
print(distance)
