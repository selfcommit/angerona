<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="password &amp; snippet sharing utility">
    <meta name="author" content="Nextraztus">
    <link rel="shortcut icon" href="${request.static_url('angerona:static/favicon.png')}">

    <title>Angerona</title>

    <link href="${request.static_url('angerona:static/bootstrap.min.css')}" rel="stylesheet">
    <link href="${request.static_url('angerona:static/theme.css')}" rel="stylesheet">
    <link href="${request.static_url('angerona:static/shilgh/styles/shCore.css')}" rel="stylesheet">
    <link href="${request.static_url('angerona:static/shilgh/styles/shThemeDefault.css')}" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="${request.static_url('angerona:static/html5shiv.js')}"></script>
      <script src="${request.static_url('angerona:static/respond.min.js')}"></script>
    <![endif]-->
  </head>
  <body>
    <div class="angerona-tplt">
      <div class="container">
	<%block name="BlockContent"/>
        <div class="row">
          <div class="links">
            <ul>
              <li><a href="${request.route_url('home')}">Share Something</a></li>
              <li><a href="https://github.com/nextraztus/angerona/blob/master/README.md">Angerona Security Model</a></li>
              <li><a href="https://github.com/nextraztus/angerona">Source Code &amp; Licensing</a></li>
            </ul>
          </div>
        </div>
        <div class="row">
          <div class="copyright">
            Copyright &copy; 2014 Nextraztus
          </div>
        </div>
      </div>
    </div>

    <script src="${request.static_url('angerona:static/jquery.min.js')}"></script>
    <script src="${request.static_url('angerona:static/bootstrap.min.js')}"></script>
  </body>
</html>
