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
          // stuff this still has to do
          //customise labels

          //if new drug create xs and column, if old push to existing.

          $scope.druglist = new Array();
          $scope.drugcolumns = new Array();
          $scope.drugcolours = {};
          $scope.drugxs = {} ;


          _.each(drug, function(a){
            var drugname = a.drug_name ;
            var drugtime = a.datetime.format("DD/MM/YYYY HH:mm:ss");
            var drugdose = a.rates ;
            var drugclass = a.drug_type ;

            var inlist = _.indexOf($scope.druglist, drugname);
            if (inlist == '-1'){
              // drug not given before
              $scope.druglist.push(drugname);
              drugnamex = drugname + "_x";
              drugorder = $scope.druglist.length;
              var i = (drugorder * 2) - 2;
              var j = (drugorder * 2) - 1;

              //push to coloumns ot create arrays
              $scope.drugcolumns.push([drugname]);
              $scope.drugcolumns.push([drugnamex]);

              //push data
              $scope.drugcolumns[i].push(drugorder);
              $scope.drugcolumns[j].push(drugtime);

              //push to colours
              var colours = [
                {class: "antiemetic_drug", colour: "#EFBE7D"},
                {class: "induction_agent_drug", colour: '#ffe800'},
                {class: "hypnotic_drug", colour: '#FF8200'},
                {class: "hypnotic_antagonist_drug", colour: '#FF8200'},
                {class: "neuromuscular_blocking_drug", colour: '#ff7477'},
                {class: "neuromuscular_blocking_drug_antagonist", colour: '#ff7477'},
                {class: "depolarizing_neuromuscular_blocking_drug", colour: '#ff7477'},
                {class: "opioid_drug", colour: '#71C5E8'},
                {class: "opioid_antagonist", colour: '#71C5E8'},
                {class: "vasopressor_drug", colour: '#D6BFDD'},
                {class: "local_anaesthetics_drug", colour: '#AFA9A0'},
                {class: "anticholinergic_drug", colour: '#A4D65E'},
                {class: "other_drug_agents", colour: '#ffffff'},
              ];
              //var nextcolour = _.where(colours, drugclass);
              var something = {class: drugclass};
              var nextcolour = _.findWhere(colours, something);
              $scope.drugcolours[drugname] = nextcolour.colour;

              //push to xs so it plots
              $scope.drugxs[drugname] = drugnamex;


            } else {
              // drug already given add to the array
              var drugord = _.indexOf($scope.druglist, drugname);
              var drugorder = drugord + 1;

              var i = (drugorder * 2) - 2;
              var j = (drugorder * 2) - 1;

              drugnamex = drugname + "_x";
              //push data
              $scope.drugcolumns[i].push(drugorder);
              $scope.drugcolumns[j].push(drugtime);
            };

          });

          var drugdata = {
            xFormat: '%d/%m/%Y %H:%M:%S',
            xs: $scope.drugxs,
            columns: $scope.drugcolumns,
            type: 'scatter',
            colors: $scope.drugcolours,
          }
          $scope.dheight = $scope.druglist.length * 15;
          return drugdata;


        }

          var chart;

          patientLoader().then(function(patient){
          newColumns = createColumns(patient.episodes[0].observation);
          newgasses = creategasses(patient.episodes[0].gases);
          newvents = ventsettings(patient.episodes[0].ventilators);
          newlines = gridlines(patient.episodes[0].anaesthetic_technique);
          newdrugs = drugs(patient.episodes[0].given_drug);

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
          opacity: 1,
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
              peep_airway_pressure: '#E4EDF6' ,
            },
            types: {
            peak_airway_pressure: 'area-spline',
            peep_airway_pressure: 'area-spline',
            },
            groups:[['peak_airway_pressure', 'peep_airway_pressure']],
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
            xFormat: '%d/%m/%Y %H:%M:%S',
            xs: newdrugs.xs,
            columns : newdrugs.columns,
            type: 'scatter',
            colors: newdrugs.colors,
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
                  var label = $scope.druglist[d-1];
                  return label;
                },
                //values: [1,2,3,4], //this needs to come from a function in the future
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
            height: $scope.dheight,
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
            newdrugs = drugs(patient.episodes[0].given_drug);


            //set first and last time for x axis
            $scope.firstobs = newColumns[4][1];
            $scope.lastobs = newColumns[4][newColumns[4].length-1];

            drugchart.axis.range({max: {x: $scope.lastobs}, min: {x: $scope.firstobs}, });
            //chart.grid(newlines);

                chart.load({
                    columns: newColumns,
                    grid: newlines,
                });
                chart2.load({
                    columns: newgasses,
                });
                chart3.load({
                    columns: newvents,
                });
                drugchart.load({
                    columns : newdrugs.columns,
                    xs: newdrugs.xs,
                    colors: newdrugs.colors,
                });

          });

        }, 10000);


});
