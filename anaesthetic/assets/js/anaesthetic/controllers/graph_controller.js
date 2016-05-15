angular.module('opal.controllers').controller(
    'GraphController',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader, patientLoader
          ){

        setInterval(function(){
          patientLoader().then(function(patient){
                $scope.patient = patient;
                $scope.observation_chart.data.raw = $scope.patient.episodes[0].observation;
                // $scope.observation_chart.context.graph.axes.y.options = $scope.patient.episodes[0].given_drug.map(function(a){
                //     return a.drug_name;
                // });
                // $scope.observation_chart.redraw();
          });
        }, 3000);

        $scope.observation_chart = new window.NH.NHGraphLib('#observations');

        // var drugs_graph = new window.NH.NHGraph();
        // drugs_graph.options.keys = ['rates'];
        // drugs_graph.axes.y.min = 0;
        // drugs_graph.axes.y.max = 100;
        // drugs_graph.axes.y.type = 'label';
        // drugs_graph.style.axis_label_text_padding = 0;
        // drugs_graph.axes.y.options = $scope.patient.episodes[0].given_drug.map(function(a){
        //     return a.drug_name;
        // });
        // drugs_graph.style.dimensions.height = 300;
        // drugs_graph.style.data_style = 'stepped';

        // var events_graph = new window.NH.NHGraph();
        // events_graph.options.keys = ['event'];
        // events_graph.axes.y.min = 0;
        // events_graph.axes.y.max = 2;
        // events_graph.style.axis.x.hide = true;
        // events_graph.style.axis.y.hide = true;
        // events_graph.style.label_width = 100;
        // events_graph.style.margin.left = 100;
        // events_graph.axes.y.type = 'graphic';
        // events_graph.axes.y.options = ['this', 'is'];
        // events_graph.style.dimensions.height = 50;
        // events_graph.style.data_style = 'graphic';
        // events_graph.options.graphic = 'http://localhost:8000/icon-event.png';
        // events_graph.drawables.background.data = [
        //     {
        //         'class': 'event',
        //         s: 0,
        //         e: 2
        //     }
        // ]
        //
        var bp_pulse_graph = new window.NH.NHGraph();
        bp_pulse_graph.options.keys = ['pulse', ['bp_systolic', 'bp_diastolic']];
        bp_pulse_graph.options.label = 'Pulse, Blood Pressure';
        bp_pulse_graph.options.measurement = '';
        bp_pulse_graph.axes.y.min = 30;
        bp_pulse_graph.axes.y.max = 220;
        bp_pulse_graph.style.dimensions.height = 300;
        bp_pulse_graph.style.data_style = 'multi';
        // bp_pulse_graph.style.axis.x.hide = true;

        var oxygen_out_graph = new window.NH.NHGraph();
        oxygen_out_graph.options.keys = ['resp_rate'];
        oxygen_out_graph.options.label = 'RR';
        oxygen_out_graph.options.measurement = '';
        oxygen_out_graph.axes.y.min = 0;
        oxygen_out_graph.axes.y.max = 40;
        oxygen_out_graph.style.dimensions.height = 300;
        oxygen_out_graph.style.data_style = 'linear';
        oxygen_out_graph.style.axis.x.hide = true;

        var oxygen_in_graph = new window.NH.NHGraph();
        oxygen_in_graph.options.keys = ['sp02'];
        oxygen_in_graph.options.label = 'SpO2';
        oxygen_in_graph.options.measurement = '';
        oxygen_in_graph.axes.y.min = 0;
        oxygen_in_graph.axes.y.max = 100;
        oxygen_in_graph.style.dimensions.height = 300;
        oxygen_in_graph.style.data_style = 'linear';
        oxygen_in_graph.style.axis.x.hide = true;

        var observations_focus = new window.NH.NHFocus();
        // var events_focus = new window.NH.NHFocus();
        var drugs_context = new window.NH.NHContext();
        drugs_context.graph = bp_pulse_graph;
        drugs_context.style.margin.bottom = 100;
        // drugs_context.style.margin.top = 0;
        // drugs_context.style.margin.left = 100;
        observations_focus.graphs.push(oxygen_out_graph);
        observations_focus.graphs.push(oxygen_in_graph);
        // events_focus.graphs.push(events_graph);

        // observations_focus.title = '';
        // observations_focus.style.margin.left = 100;
        $scope.observation_chart.context = drugs_context;
        $scope.observation_chart.focus = observations_focus;

        $scope.observation_chart.data.raw = $scope.patient.episodes[0].observation;
        $scope.observation_chart.init();
        $scope.observation_chart.draw();

        // events_focus.title = '';
        // $scope.events_chart.focus = events_focus;
        // $scope.events_chart.data.raw = data;
        // $scope.events_chart.style.margin.top = 0;
        // $scope.events_chart.style.padding.top = 0;
        // $scope.events_chart.init();
        // $scope.events_chart.draw();
});
