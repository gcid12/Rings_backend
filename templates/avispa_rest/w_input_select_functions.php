<script>
$("#input_select_<?php echo $FieldOrder; ?>").chosen({width: "100%"}); 
	
$(document).ready(function() {

	
	/*
	@USAGE urlo="http://anyurl.com/anyuser/equiposfutbol?fields=NombreDelEquipo";
	*/
	
	//The FieldSource should have a "fields" indicated
	var urlo="<?php echo $FieldSource; ?>";
	
	//Select widget can't work without a source
	if(urlo!='undefined'){
	
		var url=urlo.split("?");
	
		//This object carries the values sent via AJAX
		var urldata = new Object();
	
		//No parameters via URL?
		if(typeof url[1]!='undefined'){
			var urlpar=url[1].split("&");
			var urlval = new Array();
		
			for(j=0;j<urlpar.length;++j){
				urlval=urlpar[j].split("=");
				urldata[urlval[0]]=urlval[1];
				urlval.length=0;
			}
		}
		urldata['method']='get';
		urldata['accept']='json';
	
	

	
		
		$.get( url[0], urldata )
		.done(function( data ) {
			var returnedData = JSON.parse(data);
			//We put the returned JSON in a global variable for chosen to be able to use it
			window.input_select_<?php echo $FieldOrder; ?>=returnedData;
			
			//By default we will grab the first field to display it as the option
			if( typeof urldata['fields']=='undefined'){
				var thefield=returnedData.fields[0].FieldName;
			}else{ //But it is better if the source is explicitly indicated by &fields=<name_of_field>
				var urlfields = urldata['fields'].split(",");
				var thefield=urlfields[0];
			}
			
			var i;
			var newoption;
			for(i=0;i<returnedData.items.length; ++i){		
				//This grabs the indicated field and displays it as the option
				
				newoption = "<option>"+returnedData.items[i][thefield]+"</option>";
				$( '#input_select_<?php echo $FieldOrder; ?>' ).append(newoption);
			
			}
		
			$('#input_select_<?php echo $FieldOrder; ?>').trigger("chosen:updated");
		
		
		},"json");
		

		
	}
	
	
});

$("#input_select_<?php echo $FieldOrder; ?>").chosen().change(function(){

	//var selection = $( "#input_select_<?php echo $FieldOrder; ?>" ).val();
	/////alert('changed to: '+ selection);
	//var selected=selection.split(",");
	//var datareturned  = window.input_select_<?php echo $FieldOrder; ?>;
	 
	//for(k=0;k<selected.length;++k){
	// 	//selected[k]
	//}
	 
	//for(k=0;window.input_select.items.length;++k){
	//	if(window.input_select.items[k].NombreDelEquipo=)
	// alert('Rich: '+ window.input_select_<?php echo $FieldOrder; ?>);
	//}
});

</script>