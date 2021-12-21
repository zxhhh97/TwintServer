import twint
import pandas as pd 
import numpy as np

def df2list(wordsdf):
    array_data = np.array(wordsdf) 
    list_data=array_data.tolist()
    #dict_data = dict(list_data)
    return list_data

class TwintSearch():
    def __init__(self):
        self.c = twint.Config()

    @staticmethod
    def __get_param2type():
        valid_config_opts = ["Username","User_id","Search","Geo","Location","Near","Lang","Year","Since","Until","Email","Phone","Verified","Custom",
                            "Show_hashtags","Limit","Count","Stats","To","All","User_full","Profile_full","Retries_count","Images",
                            "Videos","Media","Lowercase","Proxy_host","Proxy_port","Proxy_type","Tor_control_port","Tor_control_password",
                            "Retweets","Popular_tweets","Native_retweets","Min_likes","Min_retweets","Min_replies","Links","Source",
                            "Members_list","Filter_retweets"]
        optstype = {}
        optstype[str] = "Username,User_id,Search,Geo,Near,Lang,Year,Since,Until,To,All,Format,Proxy_host,Proxy_type,Tor_control_password,Links,Source,Members_list".split(',')
        optstype[bool] = "Location,Email,Phone,Verified,Show_hashtags,Count,Stats,User_full,Profile_full,Images,Videos,Media,Lowercase,Retweets,Popular_tweets,Native_retweets,Filter_retweets".split(',')
        optstype[int] = "Limit,Retries_count,Proxy_port,Tor_control_port,Min_likes,Min_retweets,Min_replies".split(',')
        optstype[dict] = ["Custom"]
        param2type = {name.strip():typ for typ, namelist in optstype.items() for name in namelist }
        return param2type

    @staticmethod
    def __process_type(val,type_class):
        if isinstance(val,type_class):
            return val
        if type_class == bool and val in ["True","False","true","false"]:
            return eval(val.capitalize())
        if type_class == int:
            try:val = int(val)
            except: return None
        if type_class == str:
            try:val = str(val)
            except: return None
        if type_class == dict:
            try:
                val = json.loads(val)
                if not isinstance(val,dict):return None
            except:return None 
        return val
        
    def __add_param_to_config(self, kw):
        c = self.c
        param2type = self.__get_param2type()
        error_param = {}
        for key,origin_val in kw.items():
            key = key.strip()
            if key not in param2type:
                error_param[key] = f"Invalid keyword. Valid keywords:[{','.join(param2type.keys())}]"
            elif not origin_val:
                error_param[key] = f"None value: \{ {key}:{origin_val}\}"
            else:
                val = self.__process_type(origin_val,param2type[key])
                if val is None:
                    msg =  f"Wrong Type of param '{key}' with value={origin_val}, which should be {param2type[key]}"
                    error_param[key] = msg
                    continue
                elif isinstance(val,str):
                    if key == "Username" and "@" in val:
                        val = val.replace("@","")
                        val = val.strip()
                    exec(f"c.{key} = '{val}'")
                if isinstance(val,int) or isinstance(val,float) or isinstance(val,bool):
                    exec(f"c.{key} = {val}")
        
        if error_param:
            msg = ";".join(["Keyword '{}' has error msg: {}".format(key,value) for key,value in error_param.items()])
            raise Exception(msg)
        self.c = c


    def search_username_tweets(self, kw):
        print(kw)
        #c.Store_object = True
        #c.Pandas = True
        try:
            self.__add_param_to_config(kw)
            self.c.Pandas = True
            twint.run.Search(self.c)
            Tweets_df = twint.storage.panda.Tweets_df
            return Tweets_df
        except Exception as err:
            return {"Error":str(err)}

        ### Output
        #tweets = twint.output.tweets_list
        #print(twint.storage.panda.Tweets_df)
        #tweets = df2list(Tweets_df)
        #Tweets_df.to_csv("res.csv")   

    @staticmethod
    def get_replies_to(ocid = "1357026574936248322",username = "mikepompeo"):
        # unused
        from collections import Counter
        mother = ocid
        replies = twint.Config()
        replies.Since = "2021-02-03"
        replies.Pandas = True
        replies.To = "@"+username
        replies.Hide_output = True
        twint.run.Search(replies)
        df = twint.storage.panda.Tweets_df
        df.to_csv(f"{username}.csv")
        df2 = df[df["conversation_id"]==ocid]
        df2.to_csv(f"{username}_{ocid}.csv")

        return df2



if __name__ == "__main__":
    res = TwintSearch().search_username_tweets(dict(Username = "elonmusk",Limit=20, Since="2021-12-11 21:58:32"))
    print(res)