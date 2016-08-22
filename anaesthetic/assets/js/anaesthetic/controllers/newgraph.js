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

        var creategasses = function(anaesthetics){
            var columns = [
              ["expired_oxygen"], ["inspired_oxygen"], ["expired_aa"], ["expired_carbon_dioxide"], ["datetime"]
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

        var ventsettings = function(anaesthetics){
            var columns = [
              ["peak_airway_pressure"], ["peep_airway_pressure"], ["tidal_volume"], ["rate"], ["datetime"]
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
            ["datetime", '18/08/2016 11:10:00', '18/08/2016 11:15:00', '18/08/2016 11:20:00',]
          ];

          var chart;

          patientLoader().then(function(patient){
          newColumns = createColumns(patient.episodes[0].observation);
          newgasses = creategasses(patient.episodes[0].gases);
          newvents = ventsettings(patient.episodes[0].ventilators);



         chart = c3.generate({

          bindto: '#chart',
          legend: {
            show: false
          },

          data : {
            x: 'datetime',
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

          },

        grid: {
            x: {
              lines: [
                {value: "22/08/2016 12:50:00", text: 'Induction' },
                {value: "22/08/2016 12:55:00", text: 'Block' },
                {value: "22/08/2016 13:15:00", text: 'KTS' },
              ],
            },
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: {
                fit: true,
                format: '%d/%m %H:%M'
              },
            },
            y: {
              min: 35,
              max: 240,
              show: true,
            },

            y2: {
              show: true,
              min: 40,
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

          line :{
            show: false,
          },


          zoom: {
        		enabled: true,
            onzoomend: function(d){
            		chart2.zoom(d);
            }
          },



        }),

        chart2 = c3.generate({
          bindto: '#gaschart',
          legend: {
            show: false
          },

          data: {
            x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            columns: newgasses,
            axes: {
              expired_aa: 'y2',
              expired_carbon_dioxide: 'y2',
            },
          },
          size: {
            height: 150,
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: { format: '%d/%m %H:%M' },
              show: true,
            },

            y: { //oxygen, air, n20
              min: 0,
              max: 100,
              tick: {
                values: [25, 50, 75, 100]
              },
              padding: {
                top: 0,
                bottom: 0,
              },
              },



            y2: { //etaa, C02
              show: true,
              min: 0,
              max: 10.0,
              tick: {
                values: [2,4,6,8,10]
              },
              padding: {
                top: 0,
                bottom: 0,
              },
            },
          },

          subchart: {
            show: true,
            onbrush: function (d) {
              chart2.brush(d);
            },
            size: {
              height: 20,
            },
          },


        });

        chart3 = c3.generate({
          bindto: '#ventchart',
          legend: {
            show: false
          },

          data: {
            x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            columns: newvents,
            axes: {
              tidal_volume: 'y2',
            },
          },
          size: {
            height: 100,
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: { format: '%d/%m %H:%M' },
              show: false,
            },

            y: { //oxygen, air, n20
              min: 0,
              max: 30,
              tick: {
                values: [10, 20, 30,]
              },
              padding: {
                top: 0,
                bottom: 0,
              },
            },

            y2: { //etaa, C02
              show: true,
              min: 0,
              // max: 700
              padding: {
                //top: 100,
                bottom: 0,
              },
            },
          },

        });
      });

        setInterval(function () {
          patientLoader().then(function(patient){
            newColumns = createColumns(patient.episodes[0].observation);
            newgasses = creategasses(patient.episodes[0].gases);
            newvents = ventsettings(patient.episodes[0].ventilators);


                chart.load({
                    columns: newColumns,
                });
                chart2.load({
                    columns: newgasses,
                });
                chart3.load({
                    columns: newvents,
                });

          });

        }, 10000);


});
