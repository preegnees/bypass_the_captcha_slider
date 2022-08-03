# bypass_the_captcha_slider
Explanation of how to bypass the captcha slider by **"Template Matching"** in OpenCV, on the example of the site coinmarketcap.com.

This file can be used through a web server:
```
@app.route('/', methods=['POST'])
def hello():
	body = request.get_json()
	img_base64 = body['img']
	img_bytes = base64.b64decode(img_base64)
	return get_distance(img_bytes)
```

[...]* - search in code.

1. We write the received bytes to a file and get a picture.
2. Using opencv to read in matrix form.
3. [1]* we determine the size of the detail by eye, it is usually on the left side. We get the width, height, initial position x and y.
4. [2]* then we crop the detail, get it separately. We do the same with the rest of the part. We have two separate parts.
5. [3]* when getting the variable "..._cunny", we have to run it a couple of times (with different captchas) to find the optimal value of the parameters (the second and third arguments). In order to see the result of the run, you can simply add the code so that it saves the result and thus finds the optimal value for your site's captcha.
6. after finding the optimal measurements, we have the value x of the value, the distance we will need to move the part.

Captcha interception can be done using the "puppeteer" (js) library. For example:
```
page.on('response', async response => {
	const status = response.status()
	if ((status >= 300) && (status <= 399)) {
		console.log('Redirect from', response.url(), 'to', response.headers()['location'])
	}
	const url = response.url();
	if (response.request().resourceType() === 'image') {
		response.buffer().then(file => {
			const fileName = url.split('/').pop();
			// filtering all images that come from the server
			if (fileName.endsWith('.png')
				&& fileName.length > 30
				&& !fileName.endsWith('optimized.png')
				&& fileName != page_captha_old) {
				const resp = get_distance(file);
				console.log(fileName)
				page_captha_old = fileName
				distance = resp
			}
		});
	}
});
```

Moving the detail can be done by the code, here we use difference x (distance):
```
await page.mouse.move(handle.x + parseInt(distance) + 22, handle.y + handle.height / 2, { steps: 1 })
```
In what form do we intercept the captcha by the client:

![captcha](https://github.com/preegnees/bypass_the_captcha_slider/blob/main/captcha.PNG)


In my opinion, this method can be universal.
