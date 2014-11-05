<%inherit file="angerona:templates/base.mak" />
<%block name="BlockContent">
        <div class="row">
          <div class="col-md-10">
            <div class="content">
              <h2><a href="${uniqurl}">${uniqurl}</a></h2>
<%
if views_remain == 1:
  plural=''
else:
  plural='s'
%>

              <p>This link is good for ${friendly_time} or ${views_remain} view${plural}, whichever comes first.</p>
              <p><br/>Would you like to <a href="${request.route_url('home')}">share something again?<a/></p>
            </div>
          </div>
        </div>
</%block>

