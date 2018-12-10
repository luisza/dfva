(function ($) {
	 $(document).ready(function(){
		 var btns=$(document).find('[data-fva="true"]');
		 $.each(btns, function(index, btn){
			 btn=$(btn);
			 var seDebeAutenticar = 'False';
			 var dominio=btn.data('dominio');
			 if(dominio==undefined){
				 dominio=location.protocol+"//"+location.host;
			 }
			 
			 var ayuda=btn.data('img_ayuda');
			 if (ayuda == undefined){
				 ayuda=dominio + "/static/Imagenes/Ayuda.png";
			 }
			 var url_consulta_firma=btn.data('urlconsultafirma');
			 if(url_consulta_firma==undefined){
				 url_consulta_firma=dominio+"/Firmador/ConsulteLaFirma";
			 }
			 var img_autenticador=btn.data('img_autenticador');
			 if(img_autenticador==undefined){
				img_autenticador = dominio+"/static/Imagenes/Autenticador-v2.png";
			 }
			 var img_firma=btn.data('img_firma');
			 if(img_firma==undefined){
				 img_firma = dominio+"/static/Imagenes/Firmador-v2.png";
			 }
			 var url_css=btn.data('urlcss');
			 if(url_css==undefined){
				 url_css=dominio + "/static/css/Bccr.Fva.ClienteInterno.Firmador-1.0.2.css";
			 }
			 
			 var laConfiguracion = {
		             UrlParaSolicitarLaAutenticacion: btn.data('url'),
		             UrlParaSolicitar: btn.data('url'),
		             DominioDelSitio: dominio,
		             ParaAutenticarse: btn.data('parautenticarse'),
		             MensajeDeError:btn.data('mensajedeerror'),
		             IdDelBotonDeAutenticar: btn.attr('id'),
		             Imagenes:{
		            	 Ayuda: ayuda,
		            	 Autenticador: img_autenticador,
		            	 Firma: img_firma
		             },
		             UrlConsultaFirma: url_consulta_firma,
					 UrlCSS: url_css,
		             AutenticacionRealizada: function(){
		            	 btn.fadeOut();
		            	 window.location=btn.data('successurl');
		             },
		             ObtengaLosDatosParaSolicitarLaAutenticacion: function(){},
		             AutenticacionNoRealizada: function(){}
		         };     
			 
			 
		     FvaAutenticador(laConfiguracion);
		
		     if (seDebeAutenticar=="True") {
		    	 btn.trigger("click");
		     }     
		 });
	 });
})($);
