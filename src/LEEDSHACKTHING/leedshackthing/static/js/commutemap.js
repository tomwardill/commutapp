function featureadded(feature) {
    feature.feature.geometry.transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"))
    wkt = new OpenLayers.Format.WKT();    
    polygonControl.deactivate()
    $('#noneToggle')[0].checked = true;
    
    // set the hidden inputs for map boundaries
    $('#wkt')[0].value = wkt.write(feature.feature);
}

function activate() {
    polygonControl.activate();
    polygonLayer.removeFeatures(polygonLayer.features);
}

$(document).ready(function() {
        var map, layer;
            map = new OpenLayers.Map('map');
            layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
            map.addLayers([layer, polygonLayer]);
            map.setCenter(
                new OpenLayers.LonLat(-1.5489, 53.7938).transform(
                    new OpenLayers.Projection("EPSG:4326"),
                    map.getProjectionObject()
                ), 12
            ); 
            map.addControl(new OpenLayers.Control.LayerSwitcher());
            map.addControl(new OpenLayers.Control.MousePosition());
            
            polyOptions = {sides: 4};
            polygonControl = new OpenLayers.Control.DrawFeature(polygonLayer,
                                            OpenLayers.Handler.RegularPolygon,
                                            {handlerOptions: polyOptions});
            
            polygonControl.handler.setOptions({irregular: true});
            
            polygonControl.events.register('featureadded', polygonControl, featureadded)
            
            map.addControl(polygonControl);
            
            $("#starttime").timepicker({stepMinute: 15,});
            $("#endtime").timepicker({stepMinute: 15,});
    });