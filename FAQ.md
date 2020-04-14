# Instanalysis - F.A.Q.

## General

### Why did you create this project?
There were 3 major drivers behind this project -
<ol>
<li>Instagram is a treasure trove for analytics.  Unfortunately, a lot of the browser-based analytical tools have gone pay-only and the cost is prohibitive for non-business users</li>
<li>There are many free Python-based frameworks capable of extracting data from Instagram; however, they are mostly oriented towards automation of actions (e.g. automatic likes) and tend to be too complicated for simple extraction</li>
<li>I've always wanted to work with Selenium.  This was a simple use case</li>
</ol>

## Technical Questions

### Why do you recommend using Windows for this project?
Currently, the code uses Selenium in full visual mode (ie you can actually see the Chrome window pop up and start executing actions).  
It is currently very tricky to get this working properly on a Linux-based machine:

If you want to try this on Linux, I suggest updating the __init__ routine in the IG360Scrape class to run Chrome in headless mode.
Try replacing this line
```
self.driver = webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])
```
With these lines
```
options = webdriver.ChromeOptions()
options.binary_location = config['ENVIRONMENT']['CHROMEDRIVER_PATH']
options.add_argument('headless')
self.driver = webdriver.Chrome(chrome_options=options)
```

### Does this script use the Instagram API?
No.  The login is used only to access the follower/follwing popups and so that you can infinitely scroll through the posts

### Why should I use a VPN?
While this package does not use the Instagram API, there is still a very small chance you could be IP blocked for either making too many requests or using too many logins from the same IP address.  These bans are usually temporary, but you might ruin a family member's day while playing around with scripts.
To be pefectly safe -
<ul>
<li>Use a VPN (and refresh the connection every few days)</li>
<li>Login with an unimportant account</li>
</ul>

### What am I supposed to do with these JSON files?
Right now the notebooks generate two types of files -
<ol>
<li>Full profile for a single account (these start with "fp_")</li>
<li>Details for multiple posts belongning to an account (these start with "ps_")</li>
</ol>

For now I've been processing / testing output in Apache Spark by way of Databricks.  If you have a free Databricks account, try the following code to load a profile JSON - <br>

```
fn_fp = '(put your fp JSON filename here)'

df_fp = spark.read.json('/FileStore/tables/' + fn_fp)
display(df_fp.head(5))
```
The post files contain nested JSON data and require a little more processing -

```
fn_ps = '(put your ps JSON filename here)'

from pyspark.sql.functions import col, explode, from_json, length, substring
from pyspark.sql.functions import monotonically_increasing_id, get_json_object, when, expr
from pyspark.sql.types import TimestampType, IntegerType

df_ps = spark.read.json('/FileStore/tables/' + fn_ps)

df_raw_posts = df_ps \
  .select(col("posts")) \
  .withColumn("posts2", explode(col("posts"))) \
  .withColumn("row_id", monotonically_increasing_id()) \
  .withColumn("posts3", when(col("row_id")==0, col("posts2")).otherwise( expr("substring(posts2, 2, length(posts2)-2)") )) \
  .select(get_json_object(col("posts3"), "$.picture_id").alias("picture_id"),
  get_json_object(col("posts3"), "$.post_date").cast(TimestampType()).alias("post_dt"),
  get_json_object(col("posts3"), "$.poster").alias("poster"),
  get_json_object(col("posts3"), "$.location").alias("location"),
  get_json_object(col("posts3"), "$.likes").cast(IntegerType()).alias("likes"),
  get_json_object(col("posts3"), "$.post").alias("post"),
  get_json_object(col("posts3"), "$.like_list").alias("like_list")
  )
display(df_raw_posts.head(5))
```
Full JSON specification and sample notebooks (without Spark) will eventually be added.

## Future Plans

### Do you plan to add automated likes, follows, etc?
No!<br>
While bots aren't strictly illegal, Instagram is cracking down hard on people who use home-grown bots or unauthorized paid services to automate engagement.  This usually comes in the form of action blocks -<br><br>
https://blog.combin.com/action-blocked-on-instagram-what-triggers-and-how-to-get-rid-of-it-70d058a366c9 <br><br>
Getting an action block once makes it more likely you will get the second one, and repeated actions blocks may lead to the suspension of your account.  Some people who are not using automation receive action blocks 
just for frequent activity, so it would not be responsible to promote activity that Instagram is clearly trying to limit.

### Are you going to add more notebook examples?
Yes


