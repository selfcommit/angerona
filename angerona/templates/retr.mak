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
</%block>
