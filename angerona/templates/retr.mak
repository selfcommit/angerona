<%inherit file="angerona:templates/base.mak" />
<%block name="BlockContent">
        <div class="row">
          <div class="col-md-10">
            <div class="content">
              <h2>Data Located</h2>
<%
if views_remain == 0:
  friendly='This was the last view of this link.'
elif views_remain > 1:
  friendly='This link is good for another {} or {} views, whichever comes first.'.format(friendly_time, views_remain)
else:
  friendly='This link is good for another {} or one more view, whichever comes first.'.format(friendly_time, views_remain)
%>
              <p>${friendly}</p>
              <br/>
% if datatype != "":
              <pre class="brush: ${datatype}" >${data}</pre>
% else:
              <pre>${data}</pre>
% endif
            </div>
          </div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="col-md-4">
          <a href="${request.route_url('retrdel', uniqid=uniqid)}">
            <button class="btn btn-default">Delete this data immediately.</button>
          </a>
        </div>
    <script src="${request.static_url('angerona:static/shilgh/scripts/shCore.js')}"></script>
    <script src="${request.static_url('angerona:static/shilgh/scripts/shAutoloader.js')}"></script>
    <script type="text/javascript">
	var sr = "${request.static_url('angerona:static/shilgh/scripts/shBrush')}";
	SyntaxHighlighter.autoloader(
	  ['as3',sr+'AS3.js'],['shell',sr+'Bash.js'],['cf',sr+'ColdFusion.js'],
	  ['csharp',sr+'CSharp.js'],['cpp',sr+'Cpp.js'],['css',sr+'Css.js'],
	  ['delphi',sr+'Delphi.js'],['diff',sr+'Diff.js'],['erl',sr+'Erlang.js'],
	  ['groovy',sr+'Groovy.js'],['js',sr+'JScript.js'],['java',sr+'Java.js'],
	  ['jfx',sr+'JavaFX.js'],['pl',sr+'Perl.js'],['php',sr+'Php.js'],
	  ['plain',sr+'Plain.js'],['ps',sr+'PowerShell.js'],['py',sr+'Python.js'],
	  ['ruby',sr+'Ruby.js'],['scala',sr+'Scala.js'],['sql',sr+'Sql.js'],
	  ['vb',sr+'Vb.js'],['xml',sr+'Xml.js']
	);
        SyntaxHighlighter.all();
        </script>
</%block>
