{% extends "mail_templated/base.tpl" %}

{% block subject %}
RECUPERAR CONTRASEÑA
{% endblock %}

{% block html %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>Recuperar contraseña</title>
  <style type="text/css">
  @media only screen and (max-width: 550px), screen and (max-device-width: 550px) {
  body[yahoo] .hide {display: none!important;}
  body[yahoo] .buttonwrapper {background-color: transparent!important;}
  body[yahoo] .button {padding: 0px!important;}
  body[yahoo] .button a {background-color: #FF5252; padding: 15px 15px 13px!important;}
  body[yahoo] .unsubscribe {display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}
  }
  /*@media only screen and (min-device-width: 601px) {
    .content {width: 600px !important;}
    .col425 {width: 425px!important;}
    .col380 {width: 380px!important;}
    }*/
  </style>
</head>

<body yahoo bgcolor="#f6f8f1",style="margin: 0; padding: 0; min-width: 100%!important;">
<table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
<tr>
  <td>
    <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
    <![endif]-->
    <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 600px;">
      <tr>
        <td bgcolor="#0056a3" class="header" style="padding: 40px 30px 40px 30px;">
          <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <div style="text-align: center;">
                <img style="padding: 0 auto;height: auto;" class="fix" src="{{ url_base }}/static/img/SICAN.png" width="200" border="0" alt="" />
              </div>
            </tr>
          </table>

        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom" style="padding: 30px 30px 30px 30px;border-bottom: 1px solid #f2eeed;">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td class="h2" style="color: #153643; font-family: sans-serif;padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;">
                Hola {{ fullname }}
              </td>
            </tr>
            <tr>
              <td class="bodycopy" style="text-align: justify; color: #153643; font-family: sans-serif;font-size: 16px; line-height: 22px;">
                Recibimos una solicitud para cambiar la contraseña de acceso a tu cuenta registrada en el sistema de
                  información SICAN, si no realizaste esta solicitud porfavor borra
                  este mensaje y accede con la contraseña que tenias previamente.
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom" style="padding: 30px 30px 30px 30px;border-bottom: 1px solid #f2eeed;">
          <table width="115" align="left" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td height="115" style="padding: 0 20px 20px 0;">
                <img style="height: auto;" class="fix" src="{{ url_base }}/static/img/cuenta.png" width="115" height="115" border="0" alt="" />
              </td>
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
            <table width="380" align="left" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td>
          <![endif]-->
          <table class="col380" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 380px;">
            <tr>
              <td>
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="bodycopy" style="color: #153643; font-family: sans-serif;font-size: 16px; line-height: 22px;">
                        <p>Email: <b>{{ email }}</b></p>
                        <p>Nueva contraseña: <b>{{ password }}</b></p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 20px 0 0 0;">
                      <table class="buttonwrapper" bgcolor="#6a9ad0" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                          <td class="button" height="45" style="text-align: center; font-size: 18px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;background:#FF5252;">
                            <a href="{{ url_base }}/recovery/confirmation/?email={{email}}&code={{code}}" style="color: #ffffff; text-decoration: none;">Cambiar contraseña</a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
                </td>
              </tr>
          </table>
          <![endif]-->
        </td>




      </tr>

      <tr>
        <td class="footer" bgcolor="#0056a3" style="padding: 20px 30px 15px 30px;">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td align="center" class="footercopy" style="font-family: sans-serif; font-size: 14px; color: #ffffff;">
                &reg; 2016, SICAN<br/>
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
    <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
    </table>
    <![endif]-->
    </td>
  </tr>
</table>

<!--analytics-->
<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
<script src="http://tutsplus.github.io/github-analytics/ga-tracking.min.js"></script>
</body>
</html>
{% endblock %}