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

        var gridlines = function(events){

          events = _.map(events, function(a){
            a.datetime =  a.datetime.format("DD/MM/YYYY HH:mm:ss");
            function newline(time, title){
              this.value = time;
              this.text = title;
            }
            var lines2 = new newline(a.datetime, a.Title);
            return lines2;
          });

          var line = {
            x:{
              lines: events,
            },
          };

          return line;

        }

        var drugs = function(drug){
          // stuff this has to do
          // created columns (drug (order), drug_x (datetime))
          // colours
          // y ticks
          // create data object

          var drugdata = {
            //x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            xs: drugxs,
            columns: [
              ["fentanyl_x", '22/08/2016 12:50:00', '22/08/2016 13:15:00', '22/08/2016 14:05:00',],
              ["atracurium_x", '22/08/2016 12:55:00', '22/08/2016 13:25:00', ],
              ["propofol_x", '22/08/2016 12:53:00',],
              ["fentanyl", 1, 1, 1,],
              ["atracurium", 3, 3],
              ["propofol", 2],
            ],
            type: 'scatter',
            colors: drugcolors,
          }
          //if new drug create xs and column, if old push to existing.
          var druglist;
          var drugcolumns;

          _.each(drug, function(a){
            drugname = a.drugname
            drugtime = a.datetime
            drugdose = a.rates

            var inlist = _.find (druglist, drugname

            function drugorder (drugnm){
              a = _.findidex(druglist, drugnm);
              b = a + 1;
              return b;
            }

            if (inlist == false){
              // drug not given before
              druglist.push(drugname);
              var drugorder = new drugorder(drugname);
              drugnamex = drugname + "_x";

              //push to coloumns ot create arrays
              drugcolumns.push(drugname);
              drugcolumns.push(drugnamex);

              //push data
              drugcolumns.drugname.push(drugorder);
              drugcolumns.drugnamex.push(drugtime);

            } else {
              // drug already given add to the array
              var drugorder = new drugorder(drugname);

              drugnamex = drugname + "_x";

              //push data
              drugcolumns.drugname.push(drugorder);
              drugcolumns.drugnamex.push(drugtime);

            };

          });

          narcos = _.map(drug, function(b){

          });


        }

          var chart;

          patientLoader().then(function(patient){
          newColumns = createColumns(patient.episodes[0].observation);
          newgasses = creategasses(patient.episodes[0].gases);
          newvents = ventsettings(patient.episodes[0].ventilators);
          newlines = gridlines(patient.episodes[0].anaesthetic_technique);

          chart_padding = 75;
        chart = c3.generate({

          bindto: '#chart',
          legend: {
            show: false
          },
          padding:{
            left: chart_padding,
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

          grid: newlines,

          axis: {
            x: {
              type: 'timeseries',
              tick: {
                fit: false,
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
        }),

        chart2 = c3.generate({
          bindto: '#gaschart',
          legend: {
            show: false
          },
          padding:{
            left: chart_padding
          },

          data: {
            x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            columns: newgasses,
            axes: {
              expired_aa: 'y2',
              expired_carbon_dioxide: 'y2',
            },
            colors: {
              expired_oxygen: "#B2BEB5" ,
              inspired_oxygen: "#B2BEB5" ,
              expired_aa: '#C46210' ,
              expired_carbon_dioxide: '#1B1B1B' ,
            },
          },
          size: {
            height: 150,
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: {
                format: '%d/%m %H:%M',
                fit: false,
              },
              show: true,
            },

            y: { //oxygen, air, n20
              //min: 0,
              max: 100,
              tick: {
                values: [25, 50, 75, 100]
              },
              padding: {
                top: 0,
                //bottom: 0,
              },
              },



            y2: { //etaa, C02
              show: true,
              min: 0,
              //max: 10.0,
              tick: {
                values: [2,4,6,8,10]
              },
              padding: {
                //top: 0,
                bottom: 0,
              },
            },
          },

          subchart: {
            show: true,
            onbrush: function (d) {
              chart.zoom(d);
              chart3.zoom(d);
              drugchart.zoom(d);
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
          padding:{
            left: chart_padding
          },

          data: {
            x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            columns: newvents,
            axes: {
              tidal_volume: 'y2',
            },
            colors: {
              rate: '#007FFF' ,
              tidal_volume: '#66FF00' ,
              peak_airway_pressure: '#FF007F' ,
              peep_airway_pressure: '#FF007F' ,
            },
            types: {
            peak_airway_pressure: 'area-spline',
            //peep_airway_pressure: 'area-spline',
            },
            //groups:[['peak_airway_pressure', 'peep_airway_pressure']],
          },
          size: {
            height: 100,
          },

          axis: {
            x: {
              type: 'timeseries',
              tick: {
                fit: false,
                format: '%d/%m %H:%M'
              },
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

        drugchart = c3.generate({
          bindto: '#drugchart',
          legend: {show: false},
          padding:{
            left: chart_padding
          },
          opacity: 1,
          point: {
            r: 5,
            opacity: 1,
          },
          data: {
            //x: 'datetime',
            xFormat: '%d/%m/%Y %H:%M:%S',
            xs: { //use x value to sort order
              fentanyl: 'fentanyl_x',
              propofol: 'propofol_x',
              atracurium: 'atracurium_x',
            },
            columns: [
              ["fentanyl_x", '22/08/2016 12:50:00', '22/08/2016 13:15:00', '22/08/2016 14:05:00',],
              ["atracurium_x", '22/08/2016 12:55:00', '22/08/2016 13:25:00', ],
              ["propofol_x", '22/08/2016 12:53:00',],
              ["fentanyl", 1, 1, 1,],
              ["atracurium", 3, 3],
              ["propofol", 2],
              // ["fentanyl", 'fentanyl','fentanyl','fentanyl',],
              // ["atracurium", 'propofol','propofol',],
              // ["propofol", 'atracurium',],
            ],
            type: 'scatter',
            colors: {
              fentanyl: '#71C5E8',
              propofol: '#FEDD00',
              atracurium: '#ff6666',
            },
          },
          axis: {
            x: {
              type: 'timeseries',
              tick: {
                format: '%d/%m %H:%M',
                fit: false,
              },


            },
            y: {
              inverted: true,

              tick: {
                format: function(d){
                  //needs to be replaced by something dymanic and not hard coded!
                  //case x: return $scope.something[x-1]??
                  switch(d){
                    case 1:
                      return "fentanyl"
                    case 2:
                      return "propofol"
                    case 3:
                      return "atracurium"

                  }
                },
                values: [1,2,3], //this needs to come from a function in the future
              },
              padding: {
                top: 5,
                bottom: 5,
              },
            },
            y2: {
              //we'll use y2 to display total dose
              default: [0,4],
              tick: {
                values: [0.5,1.5,2.5,3.5], //this needs to come from a function in the future
              },
              show: true,
            },
          },
          size: {
            //height to be function of number of drugs (coloums/2 ?)
            height: 80,
          },
          grid: {
            y2: {
              show: true,
            },
          },
        });

      });

        setInterval(function () {
          patientLoader().then(function(patient){
            newColumns = createColumns(patient.episodes[0].observation);
            newgasses = creategasses(patient.episodes[0].gases);
            newvents = ventsettings(patient.episodes[0].ventilators);
            newlines = gridlines(patient.episodes[0].anaesthetic_technique);


            //set first and last time for x axis
            $scope.firstobs = newColumns[4][1];
            $scope.lastobs = newColumns[4][newColumns[4].length-1];

            drugchart.axis.range({max: {x: $scope.lastobs}, min: {x: $scope.firstobs}, });
            //chart.grid(newlines);

                chart.load({
                    columns: newColumns,
                    grid: newlines
                });
                chart2.load({
                    columns: newgasses,
                });
                chart3.load({
                    columns: newvents,
                });
                drugchart.load({
                  //load min max times
                });

          });

        }, 10000);


});
