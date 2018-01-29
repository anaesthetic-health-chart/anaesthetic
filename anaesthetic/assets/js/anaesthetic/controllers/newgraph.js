angular.module('opal.controllers').controller(
    'newgraph',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, patientLoader
          ){



        var dateformat = "DD/MM/YYYY HH:mm:ss";
        var interval;

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
          // calculate total doses for each drug

          //if new drug create xs and column, if old push to existing.

          $scope.druglist = new Array();
          $scope.drugcolumns = new Array();
          $scope.drugcolours = {};
          $scope.drugxs = {} ;
          $scope.labels = new Array(); //array for labels

          //set up stuff for infusions


          _.each(drug, function(a){
            var drugname = a.drug_name ;
            var drugtime = a.datetime.format("DD/MM/YYYY HH:mm:ss");
            var drugclass = a.drug_type ;
            var drugdose = a.dose ;

            function capitalizeEachWord(str) {
                return str.replace(/\w\S*/g, function(txt) {
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                });
            }

            drugclass = capitalizeEachWord(drugclass);

            //push dose to array for labels
            $scope.labels.push(drugdose);

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
              // var colours = [
              //   {class: "antiemetic_drug", colour: "#EFBE7D"},
              //   {class: "induction_agent_drug", colour: '#ffe800'},
              //   {class: "hypnotic_drug", colour: '#FF8200'},
              //   {class: "hypnotic_antagonist_drug", colour: '#FF8200'},
              //   {class: "neuromuscular_blocking_drug", colour: '#ff7477'},
              //   {class: "neuromuscular_blocking_drug_antagonist", colour: '#ff7477'},
              //   {class: "depolarizing_neuromuscular_blocking_drug", colour: '#ff7477'},
              //   {class: "opioid_drug", colour: '#71C5E8'},
              //   {class: "opioid_antagonist", colour: '#71C5E8'},
              //   {class: "vasopressor_drug", colour: '#D6BFDD'},
              //   {class: "local_anaesthetics_drug", colour: '#AFA9A0'},
              //   {class: "anticholinergic_drug", colour: '#A4D65E'},
              //   {class: "other_drug_agents", colour: '#ffffff'},
              // ];

              //stuff to do
              // 1 find a better way of doing this
              //have some reminder to change this if we change class names

              var colours = [
                {class: "Antiemetic Drug", colour: "#EFBE7D"},
                {class: "Induction Agent Drug", colour: '#ffe800'},
                {class: "Hypnotic Drug", colour: '#FF8200'},
                {class: "Hypnotic Antagonist Drug", colour: '#FF8200'},
                {class: "Neuromuscular Blocking Drug", colour: '#ff7477'},
                {class: "Neuromuscular Blocking Drug Antagonist", colour: '#ff7477'},
                {class: "Depolarizing Neuromuscular Blocking Drug", colour: '#ff7477'},
                {class: "Opioid Drug", colour: '#71C5E8'},
                {class: "Opioid Antagonist", colour: '#71C5E8'},
                {class: "Vasopressor Drug", colour: '#D6BFDD'},
                {class: "Local Anaesthetics Drug", colour: '#AFA9A0'},
                {class: "Anticholinergic Drug", colour: '#A4D65E'},
                {class: "Other Drug Agents", colour: '#ffffff'},
              ];
              //var nextcolour = _.where(colours, drugclass);
              var something = {class: drugclass};
              var nextcolour = _.findWhere(colours, something);
              //debugger;
              if (nextcolour == null){
                $scope.drugcolours[drugname] = '#736969';
              } else {
                $scope.drugcolours[drugname] = nextcolour.colour;
              }

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

          function drawlabels(chartInternal){
            var textLayer = drugchart.internal.main.select('.' + c3.chart.internal.fn.CLASS.chartTexts);
            _.each(drugchart.internal.mainCircle, function(a){
              _.each(a, function(){
                textLayer.select('text').remove();
              })
            })
             _.each(drugchart.internal.mainCircle, function(point){
               _.each(point, function(p){
                 var d3point = d3.select(p);
                 var ind = _.findIndex(drugchart.internal.mainCircle, point);
                 textLayer
                     .append('text')
                     // center horizontally and vertically
                     .style('text-anchor', 'middle').attr('dy', '.2em')
                     .text($scope.labels[ind])
                     // same as at the point
                     .attr('x', d3point.attr('cx')).attr('y', d3point.attr('cy'));
               })
             })
          }

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
              bp_systolic: '#DA291C' ,
              bp_diastolic: '#DA291C' ,
              pulse: '#78BE20' ,
              Sp02: '#FAE100' ,
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
              expired_oxygen: "#768692" ,
              inspired_oxygen: "#768692" ,
              expired_aa: '#ED8B00' ,
              expired_carbon_dioxide: '#231f20' ,
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
              rate: '#330072' ,
              tidal_volume: '#ED8B00' ,
              peak_airway_pressure: '#AE2573' ,
              peep_airway_pressure: '#AE2573' ,
            },
            // types: {
            // peak_airway_pressure: 'area-spline',
            // peep_airway_pressure: 'area-spline',
            // },
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
            //should probably get rid of this
            labels: {
              show: false,
              // format : function(d){
              //   var label = $scope.labels[d-1];
              //   return label
              // }
              format: function (v, id, i, j) {
                var label = $scope.labels[i-1];
                return label;
              }

            }

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
                format: function(e){
                  var label = $scope.druglist[e-1];
                  return label;
                },
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
      drawlabels(drugchart.interal);

      });

        interval = setInterval(function () {
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
          drawlabels(drugchart.interal);
        }, 10000);

        $scope.$on("$routeChangeStart", function(){
          if(interval){
            clearInterval(interval);
          }
        });


});
