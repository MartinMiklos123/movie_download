// I have tried many different python libraries to fetch network traffic from website
// this is the only one which could pick up the video source link

const puppeteer = require('puppeteer');
let url_list = [];
const fs = require('fs');
const link = process.argv[2]


async function captureNetworkRequests() {
    // Launch a headless browser
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Listen for network requests
    page.on('response', response => {
		url_list.push(response.url());
        console.log('Captured URL:', response.url());
    });

    // Navigate to a website
    await page.goto(link);



    // Close the browser
    await browser.close();


	console.log(url_list);
	return url_list;
}

async function saveUrlsToFile() {
    const urls = await captureNetworkRequests();

    // Save the captured URLs to a .txt file
    const filePath = 'captured_urls.txt';
    const urlsContent = urls.join('\n'); // Join the array into a string with each URL on a new line

    // Write the URLs to the file
    fs.writeFileSync(filePath, urlsContent);

    console.log(`Captured URLs have been saved to ${filePath}`);
}

// Run the function to capture and save URLs
saveUrlsToFile();