import smtplib
from email.mime.text import MIMEText
import os

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def send_verification_email(to_email, code):
    html_content = f'''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>New Message 2</title><!--[if (mso 16)]>
        <style type="text/css">
        a {{text-decoration: none;}}
        </style>
        <![endif]--><!--[if gte mso 9]><style>sup {{ font-size: 100% !important; }}</style><![endif]--><!--[if gte mso 9]>
    <noscript>
            <xml>
            <o:OfficeDocumentSettings>
            <o:AllowPNG></o:AllowPNG>
            <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
            </xml>
        </noscript>
    <![endif]--><!--[if mso]><xml>
        <w:WordDocument xmlns:w="urn:schemas-microsoft-com:office:word">
        <w:DontUseAdvancedTypographyReadingMail/>
        </w:WordDocument>
        </xml><![endif]-->
    <style type="text/css">.rollover:hover .rollover-first {{
    max-height:0px!important;
    display:none!important;
    }}
    .rollover:hover .rollover-second {{
    max-height:none!important;
    display:block!important;
    }}
    .rollover span {{
    font-size:0px;
    }}
    u + .body img ~ div div {{
    display:none;
    }}
    #outlook a {{
    padding:0;
    }}
    span.MsoHyperlink,
    span.MsoHyperlinkFollowed {{
    color:inherit;
    mso-style-priority:99;
    }}
    a.p {{
    mso-style-priority:100!important;
    text-decoration:none!important;
    }}
    a[x-apple-data-detectors],
    #MessageViewBody a {{
    color:inherit!important;
    text-decoration:none!important;
    font-size:inherit!important;
    font-family:inherit!important;
    font-weight:inherit!important;
    line-height:inherit!important;
    }}
    .d {{
    display:none;
    float:left;
    overflow:hidden;
    width:0;
    max-height:0;
    line-height:0;
    mso-hide:all;
    }}
    @media only screen and (max-width:600px) {{.be {{ padding-right:0px!important }}  *[class="gmail-fix"] {{ display:none!important }} p, a {{ line-height:150%!important }} h1, h1 a {{ line-height:120%!important }} h2, h2 a {{ line-height:120%!important }} h3, h3 a {{ line-height:120%!important }} h4, h4 a {{ line-height:120%!important }} h5, h5 a {{ line-height:120%!important }} h6, h6 a {{ line-height:120%!important }}  .bb p {{ }} .ba p {{ }}  h1 {{ font-size:36px!important; text-align:left }} h2 {{ font-size:26px!important; text-align:left }} h3 {{ font-size:20px!important; text-align:left }} h4 {{ font-size:24px!important; text-align:left }} h5 {{ font-size:20px!important; text-align:left }} h6 {{ font-size:16px!important; text-align:left }} .bc h1 a, .bb h1 a, .ba h1 a {{ font-size:36px!important }}      .b td a {{ font-size:12px!important }}  .bb p, .bb a {{ font-size:14px!important }} .ba p, .ba a {{ font-size:14px!important }}  .w, .w h1, .w h2, .w h3, .w h4, .w h5, .w h6 {{ text-align:center!important }}     .v .rollover:hover .rollover-second, .w .rollover:hover .rollover-second, .x .rollover:hover .rollover-second {{ display:inline!important }}        .i table, .j table, .k table, .i, .k, .j {{ width:100%!important; max-width:600px!important }} .adapt-img {{ width:100%!important; height:auto!important }}        .b td {{ width:1%!important }}  .h-auto {{ height:auto!important }} }}
    @media screen and (max-width:384px) {{.mail-message-content {{ width:414px!important }} }}</style>
    </head>
    <body class="body" style="width:100%;height:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
    <div dir="ltr" class="es-wrapper-color" lang="en" style="background-color:#FAFAFA"><!--[if gte mso 9]>
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                    <v:fill type="tile" color="#fafafa"></v:fill>
                </v:background>
            <![endif]-->
    <table width="100%" cellspacing="0" cellpadding="0" class="es-wrapper" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FAFAFA">
        <tr>
        <td valign="top" style="padding:0;Margin:0">
        <table cellpadding="0" cellspacing="0" align="center" class="j" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="bc" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-top:10px;padding-right:20px;padding-bottom:10px;padding-left:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" class="be" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:20px;font-size:0px"><img src="https://ecaafec.stripocdn.email/content/guids/CABINET_6a0e298ea553326c3d4032a9bbf684aeb94b7e27c6fdb6450af199b6e5ec2c0f/images/ccdl_banner.png" alt="Logo" width="200" title="Logo" class="adapt-img" style="display:block;font-size:12px;border:0;outline:none;text-decoration:none;margin:0"></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table cellpadding="0" cellspacing="0" align="center" class="i" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="bb" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-right:20px;padding-bottom:10px;padding-left:20px;padding-top:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-top:10px;padding-bottom:10px;font-size:0px"><img src="https://ecaafec.stripocdn.email/content/guids/CABINET_6a0e298ea553326c3d4032a9bbf684aeb94b7e27c6fdb6450af199b6e5ec2c0f/images/favicon.png" alt="" width="300" class="adapt-img" style="display:block;font-size:14px;border:0;outline:none;text-decoration:none;margin:0"></td>
                        </tr>
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:10px;padding-top:20px"><h3 class="w" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:20px;font-style:normal;font-weight:bold;line-height:20px;color:#333333">Cyber@Stout Verification Code</h3></td>
                        </tr>
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px"><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;letter-spacing:0;color:#333333;font-size:14px">Welcome to the Cyber@Stout server!&nbsp;</p><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;letter-spacing:0;color:#333333;font-size:14px">Below you will find your verification code so you can get access into all of the roles the server has to offer.&nbsp;</p><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;letter-spacing:0;color:#333333;font-size:14px">Once you have verified your account please select your prefered roles in the roles channel</p></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
                <tr>
                <td align="left" style="Margin:0;padding-top:10px;padding-right:20px;padding-bottom:10px;padding-left:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px dashed #cccccc;border-right:2px dashed #cccccc;border-top:2px dashed #cccccc;border-bottom:2px dashed #cccccc;border-radius:5px" role="presentation">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-right:20px;padding-left:20px;padding-top:20px"><h2 class="w" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:26px;font-style:normal;font-weight:bold;line-height:31.2px;color:#333333">Your Verification Code</h2></td>
                        </tr>
                        <tr>
                        <td align="center" style="Margin:0;padding-top:10px;padding-right:20px;padding-left:20px;padding-bottom:20px"><h1 class="w" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:46px;font-style:normal;font-weight:bold;line-height:55.2px;color:#333333"><strong><a target="_blank" style="mso-line-height-rule:exactly;text-decoration:none;color:#5C68E2;font-size:46px" href="">FGH-123-VBN</a></strong></h1></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
                <tr></tr>
                <tr></tr>
                <tr></tr>
            </table></td>
            </tr>
        </table>
        <table cellpadding="0" cellspacing="0" align="center" class="k" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table align="center" cellpadding="0" cellspacing="0" class="ba" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:640px" role="none">
                <tr>
                <td align="left" style="Margin:0;padding-right:20px;padding-left:20px;padding-bottom:20px;padding-top:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="left" style="padding:0;Margin:0;width:600px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:35px"><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:18px;letter-spacing:0;color:#333333;font-size:12px">Cyber@Stout © 2024 Collegiate Cyber Defense League All Rights Reserved.</p><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:18px;letter-spacing:0;color:#333333;font-size:12px">712 Broadway St S, Menomonie, WI 54751</p></td>
                        </tr>
                        <tr>
                        <td style="padding:0;Margin:0">
                        <table cellpadding="0" cellspacing="0" width="100%" class="b" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr class="links">
                            <td align="center" valign="top" width="33.33%" style="Margin:0;border:0;padding-top:5px;padding-bottom:5px;padding-right:5px;padding-left:5px">
                            <div style="vertical-align:middle;display:block"><a target="_blank" href="https://cyberatstout.org" style="mso-line-height-rule:exactly;text-decoration:none;font-family:arial, 'helvetica neue', helvetica, sans-serif;display:block;color:#999999;font-size:12px">Visit Us </a>
                            </div></td>
                            <td align="center" valign="top" width="33.33%" style="Margin:0;border:0;padding-top:5px;padding-bottom:5px;padding-right:5px;padding-left:5px;border-left:1px solid #cccccc">
                            <div style="vertical-align:middle;display:block"><a target="_blank" href="https://help.cyberstout.org/misc/sso-privacy-policy/" style="mso-line-height-rule:exactly;text-decoration:none;font-family:arial, 'helvetica neue', helvetica, sans-serif;display:block;color:#999999;font-size:12px">Privacy Policy</a>
                            </div></td>
                            <td align="center" valign="top" width="33.33%" style="Margin:0;border:0;padding-top:5px;padding-bottom:5px;padding-right:5px;padding-left:5px;border-left:1px solid #cccccc">
                            <div style="vertical-align:middle;display:block"><a target="_blank" href="https://help.cyberstout.org/misc/sso-terms-of-service/" style="mso-line-height-rule:exactly;text-decoration:none;font-family:arial, 'helvetica neue', helvetica, sans-serif;display:block;color:#999999;font-size:12px">Terms of Service</a>
                            </div></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table></td>
        </tr>
    </table>
    </div>
    </body>
    </html>
    '''
    html_content = html_content.replace("FGH-123-VBN", code)
    msg = MIMEText(html_content, "html")
    msg['Subject'] = 'Cyber@Stout Verification Code'
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        if SMTP_PORT == 587:
            server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
