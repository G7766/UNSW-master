
function run_cgi(base_url, cgi) {
	if (!cgi || cgi.length === 0)
		return;
	if (cgi.charAt(0) == "#")
		cgi = cgi.substr(1);
	if (cgi.length === 0)
		return;
	var cgi_output = $(".cgi_output_display")[0];
	var cgi_source = $(".cgi_source_display")[0];
    if (/insecure/.test(cgi)) {
        cgi_source.src = "";
    } else {
        cgi_output.src = base_url + cgi;
    }

    if (/\.html$/.test(cgi)) {
        cgi_source.src = "";
    } else {
	    if (/insecure/.test(cgi)) {
	        cgi_source.src = "";
	    } else {
	        cgi_output.src = base_url + cgi;
	    }
	
	    if (/\.html$/.test(cgi)) {
	        cgi_source.src = "";
	    } else {
	        cgi_source.src = base_url + cgi + ".txt";
	        console.log($('.title_panel'));
	        $('.title_panel').text(cgi);
	        $('.title_panel').append(' ');
	        $('.title_panel').append($('<a>', {text: ' download', target: '_blank', href: base_url + cgi + ".txt"}));
	        $('.title_panel').append(' ');
	        $('.title_panel').append($('<a>', {text: ' run in new window', target: '_blank', href: base_url + cgi}));
	    }
	}
}

function show_html_source(iframe) {
 	var html_source = $(iframe).parent().parent().find(".html_source_display");
 	if (!html_source.length) {
 		html_source = $("#html_source");
 	}
   	var d = iframe.contentWindow.document;
    head_html = d.head.outerHTML.concat("\n");
    body_html = d.body.outerHTML.concat("\n");
    body_html = body_html.replace(/\s*<\/body>/mi, '\n<\/body>');
    html = head_html.concat(body_html);
    html = "<html>\n".concat(html).concat("<").concat("/html>\n");
    $(html_source).text(html);
}
