angular.module('app.services', [])

.factory('DATA', function(){


	var schools= [
		{name:'数学'}, 
		{name:'电子与信息工程'},
		{name:'艺术传媒学院'},
	]
              var subgrade=[
              	{grade:'11',num:0},
              	{grade:'12',num:0},
              	{grade:'13',num:0},
              	{grade:'14',num:0},
                            {grade:'15',num:0}
              ]
	var myStuTypes = [
		{type: 0, show: "本科"},
		{type: 1, show: "硕士"},
	]

	var  Results = [];
	var  student_data =[];
	var Equipments = [];
	var stations = null;
	return {
	    all_schools: function() {
	      return schools;
	      },
	    get_subgrade:function(){
	       return subgrade;
	     },
              
	    // get_stations: function(findName) {
	    //   for (var i = 0; i < stations.length; i++) {
	    //     if (stations[i].name === findName) {
	    //       return stations[i];
	    //     }
	    //   }
	    //   return null;
	    // },

	    all_options_search: function() {
	    	return myStuTypes;
	    },
	    all_options_pic: function(){
	    	return myOptions_pic;
	    },

	    get_Results: function() {
	    	return Results;
	    },
	    set_Results: function(results) {
	    	Results = angular.fromJson(results);
	    },
	    add_Results:function(results){
                         Results=Results.concat(results);
                  	// return JSON.stringify(Results)
	    },
	   get_student_data: function() {
	    	return student_data;
	    },
	    set_student_data: function(student_data) {
	    	student_data = angular.fromJson(student_data);
	    },
	    add_student_data:function(student_data){
                         student_data=student_data.concat(student_data);
                  	// return JSON.stringify(Results)
	    },
	    get_Equipments: function() {
	    	return Equipments;
	    },
	    set_Equipments: function(Equipment) {
	    	Equipments = angular.fromJson(Equipment);
	    },
	    add_Equipments:function(Equipment){
                        Equipments=Equipments.concat(Equipment);
                  	// return JSON.stringify(Results)
	    },
	    set_stations:function(results){
	    	stations=results; },
 	}
 	

})

.factory('Storage', function() {
    return {
        set: function(key, data) {
            return window.localStorage.setItem(key, window.JSON.stringify(data));
        },
        get: function(key) {

            return window.JSON.parse(window.localStorage.getItem(key));
        },
        remove: function(key) {
            return window.localStorage.removeItem(key);
        }
    };
})

.service('BlankService', [function(){

}]);

