angular.module('opal.controllers').controller(
    'newgraph',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader, patientLoader
          ){



        dateformat = "DD/MM/YYYY HH:mm:ss"

        var createColumns = function(anaesthetics){
            var columns = [
              ["bp_systolic"], ["bp_diastolic"], ["pulse"], ["Sp02"], ["datetime"]
            ];
            anaesthetics = _.map(anaesthetics.reverse(), function(a){
                a.datetime =  a.datetime.format("DD/MM/YYYY HH:mm:ss");
                return a;
            });


            _.each(columns, function(column){
                _.each(anaesthetics, function(anaesthetic){
                    column.push(anaesthetic[column[0].toLowerCase()]);
                });
            });

            return columns;
        }

        columns = [
            ["bp_systolic", 120, 123, 125],
            ["bp_diastolic", 60, 65, 59],
            ["pulse", 82, 69, 90],
            ["Sp02", 98, 99, 98],
            //["datetime", 1, 2, 3],
            //["datetime", moment('18/08/2016 11:10:00', dateformat).toDate(), moment('18/08/2016 11:15:00', dateformat).toDate(), moment('18/08/2016 11:20:00', dateformat).toDate(),]
            ["datetime", '18/08/2016 11:10:00', '18/08/2016 11:15:00', '18/08/2016 11:20:00',]
          ];

          var chart;

          patientLoader().then(function(patient){
          newColumns = createColumns(patient.episodes[0].observation);

          
         chart = c3.generate({

          bindto: '#chart',

          data : {
            xs: {
              bp_systolic: 'datetime',
              bp_diastolic: 'datetime',
              pulse: 'datetime',
              Sp02: 'datetime'
            },
            xFormat: '%d/%m/%Y %H:%M:%S',
            //xFormat: '%Y-%m-%d %H:%M:%S',
            columns: newColumns,

            colors: {
              bp_systolic: "red" ,
              bp_diastolic: "red" ,
              pulse: "green" ,
              sp02: "yellow" ,
            },

          type: 'scatter',
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: { format: '%d-%m %H:%M' },
            },
            y2: {
              show: true
            }
          },

          subchart: {
            show: true
          },



        });
      });

        setInterval(function () {
          patientLoader().then(function(patient){
            newColumns = createColumns(patient.episodes[0].observation);

                chart.load({
                    columns: newColumns,
                });
          });

        }, 3000);


        $scope.observation_chart = new window.NH.NHGraphLib('#observations');
        // var events_chart = new window.NH.NHGraphLib('#events');

         var drugs_graph = new window.NH.NHGraph();
         drugs_graph.options.keys = ['drug_name'];
         drugs_graph.axes.y.min = 0;
         drugs_graph.axes.y.max = 100;
         drugs_graph.axes.y.type = 'label';
         drugs_graph.style.axis_label_text_padding = 0;
         drugs_graph.axes.y.options = [
             'Propofol',
             'Fentanyl',
             'Rocuronium', 'Test'];
         drugs_graph.style.dimensions.height = 120;
         drugs_graph.style.data_style = 'linear';

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

        var bp_pulse_graph = new window.NH.NHGraph();
        bp_pulse_graph.options.keys = ['pulse',
            ['bp_systolic', 'bp_diastolic']
        ];
        bp_pulse_graph.options.label = 'Pulse, Blood Pressure';
        bp_pulse_graph.options.measurement = '';
        bp_pulse_graph.axes.y.min = 30;
        bp_pulse_graph.axes.y.max = 220;
        bp_pulse_graph.style.dimensions.height = 300;
        bp_pulse_graph.style.data_style = 'multi';
        // bp_pulse_graph.style.axis.x.hide = true;

        // var oxygen_out_graph = new window.NH.NHGraph();
        // oxygen_out_graph.options.keys = ['et', 'fico'];
        // oxygen_out_graph.options.label = 'Fi/ETAA FiCO2';
        // oxygen_out_graph.options.measurement = '';
        // oxygen_out_graph.axes.y.min = 0;
        // oxygen_out_graph.axes.y.max = 12;
        // oxygen_out_graph.style.dimensions.height = 300;
        // oxygen_out_graph.style.data_style = 'multi';
        // oxygen_out_graph.style.axis.x.hide = true;

        var oxygen_in_graph = new window.NH.NHGraph();
        oxygen_in_graph.options.keys = ['sp02'];
        oxygen_in_graph.options.label = 'SpO2';
        oxygen_in_graph.options.measurement = '';
        oxygen_in_graph.axes.y.min = 80;
        oxygen_in_graph.axes.y.max = 100;
        oxygen_in_graph.style.dimensions.height = 100;
        oxygen_in_graph.style.data_style = 'linear';
        oxygen_in_graph.style.axis.x.hide = true;

        //lets try and make a new cotext graph
        var op_event_graph = new window.NH.NHGraph(); //op event as we'll be putting event markers on it
        op_event_graph.options.keys = ['Title']
        op_event_graph.style.dimensions.height = 30;
        op_event_graph.style.data_style = 'linear';
        op_event_graph.style.axis.x.hide = true;
        op_event_graph.style.axis.y.hide = true;
        op_event_graph.style.data_style = 'graphic';
        op_event_graph.options.graphic = 'http://localhost:8000/assets/js/anaesthetic/icon-event.png';
        op_event_graph.options.keys = ['event'];


        var observations_focus = new window.NH.NHFocus();
        var events_focus = new window.NH.NHFocus();
        var drugs_context = new window.NH.NHContext();
        drugs_context.graph = op_event_graph;
        drugs_context.style.margin.bottom = 50;
        // drugs_context.style.backgroundcolor = "#C9046F";
        // drugs_context.style.margin.top = 0;
        // drugs_context.style.margin.left = 100;
        // observations_focus.graphs.push(bp_pulse_graph);
        // observations_focus.graphs.push(oxygen_out_graph);
        //observations_focus.graphs.push(drugs_graph);
        observations_focus.graphs.push(bp_pulse_graph); // make bp focus graph
        observations_focus.graphs.push(oxygen_in_graph); //make oxygen focus graph

        // events_focus.graphs.push(events_graph);

        observations_focus.title = '';
        // observations_focus.style.margin.left = 100;
        $scope.observation_chart.context = drugs_context;
        $scope.observation_chart.focus = observations_focus;

        $scope.observation_chart.data.raw = $scope.patient.episodes[0].observation.reverse().map(function(a){
            a.date_terminated = $scope.observation_chart.date_to_proper_string(a.datetime._d);
            return a;
        });
        $scope.observation_chart.init();
        $scope.observation_chart.draw();

        // events_focus.title = '';
        // events_chart.focus = events_focus;
        // events_chart.data.raw = data;
        // events_chart.style.margin.top = 0;
        // events_chart.style.padding.top = 0;
        // events_chart.init();
        // events_chart.draw();
});
