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
            columns: newColumns,

            colors: {
              bp_systolic: "red" ,
              bp_diastolic: "red" ,
              pulse: "green" ,
              Sp02: '#ffff00' ,
            },

            axes: {
              Sp02: 'y2',
            },

          type: 'scatter',
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: { format: '%d/%m %H:%M' },
            },
            y: {
              min: 35,
              max: 240,
              show: true,
            },

            y2: {
              show: true,
              min: 0,
              max: 100,
              padding: {
                top: 0,
                bottom: 0,
              },
              tick: {
                values: [100, 90, 80, 60]
              },
            },
          },

          subchart: {
            show: true,
            size: {
              height: 20,
            },
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

        }, 10000);


});
