# Recupera o código do telefone. Não mude
# O arquivo deve permanecer completamente inalterado

def retrieve_phone_code(driver) -> str:


    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("Nenhum código de confirmação de telefone encontrado.\n"
                            "Use retrieve_phone_code somente depois que o código for solicitado em seu aplicativo.")
        return code

# Verifica se o Routes está ativo e funcionando. Não mude
def is_url_reachable(url):


    import ssl
    import urllib.request

    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx) as response:

            if response.status == 200:
                 return True
            else:
                return False
    except Exception as e:
        print (e)

    return False