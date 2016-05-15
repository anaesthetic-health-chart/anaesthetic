angular.module('opal.controllers').controller(
    'GraphController',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader
          ){

            
        var observation_chart = new window.NH.NHGraphLib('#observations');
        var events_chart = new window.NH.NHGraphLib('#events');
        var data = [
            {
                'date_terminated': '2016-05-14 09:00:00',
                'blood_pressure_systolic': 120,
                'blood_pressure_diastolic': 80,
                'pulse': 80,
                'et': 4.8,
                'fico': 3.5,
                'spo': 99,
                'fio': 51,
                'drug': 'Test',
                'event': 'Foo'
            },
            {
                'date_terminated': '2016-05-14 09:05:00',
                'blood_pressure_systolic': 110,
                'blood_pressure_diastolic': 70,
                'pulse': 70,
                'et': 4.6,
                'fico': 2.4,
                'spo': 98,
                'fio': 49,
                'drug': 'Is',
                'event': 'Foo'
            },
            {
                'date_terminated': '2016-05-14 09:10:00',
                'blood_pressure_systolic': 100,
                'blood_pressure_diastolic': 60,
                'pulse': 80,
                'et': 5.1,
                'fico': 2.8,
                'spo': 100,
                'fio': 48,
                'drug': {
                    'name': 'Test',
                    'type': 'started'
                },
                'event': 'Bar'
            }
        ];
        var drugs_graph = new window.NH.NHGraph();
        drugs_graph.options.keys = ['drug'];
        drugs_graph.axes.y.min = 0;
        drugs_graph.axes.y.max = 100;
        drugs_graph.axes.y.type = 'label';
        drugs_graph.style.axis_label_text_padding = 0;
        drugs_graph.axes.y.options = [
            'Propofol',
            'Fentanyl',
            'Rocuronium', 'Test'];
        drugs_graph.style.dimensions.height = 300;
        drugs_graph.style.data_style = 'stepped';

        var events_graph = new window.NH.NHGraph();
        events_graph.options.keys = ['event'];
        events_graph.axes.y.min = 0;
        events_graph.axes.y.max = 2;
        events_graph.style.axis.x.hide = true;
        events_graph.style.axis.y.hide = true;
        events_graph.style.label_width = 100;
        events_graph.style.margin.left = 100;
        events_graph.axes.y.type = 'graphic';
        events_graph.axes.y.options = ['this', 'is'];
        events_graph.style.dimensions.height = 50;
        events_graph.style.data_style = 'graphic';
        events_graph.options.graphic = 'http://localhost:8000/icon-event.png';
        events_graph.drawables.background.data = [
            {
                'class': 'event',
                s: 0,
                e: 2
            }
        ]

        var bp_pulse_graph = new window.NH.NHGraph();
        bp_pulse_graph.options.keys = ['pulse',
            ['blood_pressure_systolic', 'blood_pressure_diastolic']
        ];
        bp_pulse_graph.options.label = 'Pulse, Blood Pressure';
        bp_pulse_graph.options.measurement = '';
        bp_pulse_graph.axes.y.min = 30;
        bp_pulse_graph.axes.y.max = 220;
        bp_pulse_graph.style.dimensions.height = 300;
        bp_pulse_graph.style.data_style = 'multi';
        bp_pulse_graph.style.axis.x.hide = true;

        var oxygen_out_graph = new window.NH.NHGraph();
        oxygen_out_graph.options.keys = ['et', 'fico'];
        oxygen_out_graph.options.label = 'Fi/ETAA FiCO2';
        oxygen_out_graph.options.measurement = '';
        oxygen_out_graph.axes.y.min = 0;
        oxygen_out_graph.axes.y.max = 12;
        oxygen_out_graph.style.dimensions.height = 300;
        oxygen_out_graph.style.data_style = 'multi';
        oxygen_out_graph.style.axis.x.hide = true;

        var oxygen_in_graph = new window.NH.NHGraph();
        oxygen_in_graph.options.keys = ['spo', 'fio'];
        oxygen_in_graph.options.label = 'SpO2 / FiO2';
        oxygen_in_graph.options.measurement = '';
        oxygen_in_graph.axes.y.min = 0;
        oxygen_in_graph.axes.y.max = 100;
        oxygen_in_graph.style.dimensions.height = 300;
        oxygen_in_graph.style.data_style = 'multi';
        oxygen_in_graph.style.axis.x.hide = true;

        var observations_focus = new window.NH.NHFocus();
        var events_focus = new window.NH.NHFocus();
        var drugs_context = new window.NH.NHContext();
        drugs_context.graph = drugs_graph;
        drugs_context.style.margin.bottom = 0;
        drugs_context.style.margin.top = 0;
        drugs_context.style.margin.left = 100;
        observations_focus.graphs.push(bp_pulse_graph);
        observations_focus.graphs.push(oxygen_out_graph);
        observations_focus.graphs.push(oxygen_in_graph);
        events_focus.graphs.push(events_graph);

        observations_focus.title = '';
        observations_focus.style.margin.left = 100;
        observation_chart.context = drugs_context;
        observation_chart.focus = observations_focus;

        observation_chart.data.raw = data;
        observation_chart.init();
        observation_chart.draw();

        events_focus.title = '';
        events_chart.focus = events_focus;
        events_chart.data.raw = data;
        events_chart.style.margin.top = 0;
        events_chart.style.padding.top = 0;
        events_chart.init();
        events_chart.draw();
});
