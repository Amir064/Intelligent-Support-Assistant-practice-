import requests
import src.config as config


def generateResponse(prompt):

    url = ( "https://api.cloudflare.com/client/v4/accounts/"
        f"{config.CLOUDFLARE_ACCOUNT_ID}/ai/run/{config.LLM_model}"
            )

    HEADERS = {
                "Authorization" : f"Bearer {config.CLOUDFLARE_API_TOKEN}"
            }    
    PAYLOUD ={"messages":[
            
            {"role":"user","content":prompt }
            ]
        }


    try:
        response = requests.post(url,headers=HEADERS,json=PAYLOUD,timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"LLM API request failed: {error}") from error

    

    try:
        data=response.json()
        answer = data["result"]["response"]
    except:
        raise RuntimeErro(
            "Invalid response received from LLM API"
        )from error

    return answer
   

if __name__=="__main__":
    res=generateResponse("salam azizam")
    print(res)
