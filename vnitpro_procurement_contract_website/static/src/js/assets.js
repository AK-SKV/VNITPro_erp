$(document).ready(function(){
	var observer = new MutationObserver(function(mutations) {
	   	mutations.forEach(function(mutation) {
	       	if (mutation.addedNodes && mutation.addedNodes.length > 0) {
	           // element added to DOM
	           	var hasClass = [].some.call(mutation.addedNodes, function(el) {
	               return el.classList.contains('modal');
	        	});
	           	if (hasClass) {
	           		var text = $('h4.modal-title').text();
	           		if (text.indexOf('Odoo') >= 0 ){
	           			$('h4.modal-title').text(text.substring(text.indexOf('Odoo')).replace('Odoo Server Error', 'Hệ thống'));
	           		}
	           	}
	       	}
	   	});
	});

	var config = {
	   	attributes: true,
	   	childList: true,
	   	characterData: true
	};
	observer.observe(document.body, config);	
});
	
