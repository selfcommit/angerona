<%inherit file="angerona:templates/base.mak" />
<%block name="BlockContent">
        <div class="row">
          <h2>That link has evaporated.</h2>
          <p>Would you like to <a href="${request.route_url('home')}">share something else?<a/></p>
        </div>
</%block>
