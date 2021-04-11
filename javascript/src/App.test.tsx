export {} 

let alreadyRunning = false;
const webdriver = require("selenium-webdriver");

const fs = require('fs');
const fetch = require("node-fetch");

// generates data to be saved as webData.tsx
// Adjust these (top of file) 
// const minPageNum = 1
// const maxPageNum = 50;
// const maxNumVehiclesToScrape = 500;

describe('scrape cmr data', () => {
  let driverSimple = undefined;
  if (!alreadyRunning) {
    alreadyRunning = true;

    const capabilityName = 'goog:chromeOptions'; // Switch to 'moz:firefoxOptions' if desired
  
    // Set up the commandline options for launching the driver.
    // In this example, I'm using various headless options.
    const browserOptions = {
      args: ['--disable-gpu', '--no-sandbox'],
    };
    //if (headless) {
    //  browserOptions.args.unshift('--headless');
    //}
    // Set up the browser capabilities.
    // Some lines could be condensed into one-liners if that's your preferred style.
    
    let browserCapabilities = webdriver.Capabilities.chrome();
    browserCapabilities = browserCapabilities.set(capabilityName, browserOptions);

    const builder = new webdriver.Builder().forBrowser('chrome');
    // Setting the proxy-server option is needed to info chrome to use proxy
    const chrome = require('selenium-webdriver/chrome');
    let option = new chrome.Options();

    // let proxyAddress = '86.145.14.192:8080';
    // option = option.addArguments(`--proxy-server=${proxyAddress}`);

    driverSimple = builder.withCapabilities(browserCapabilities).setChromeOptions(option).build();
  }
  if (driverSimple == undefined) {
    return;
  }
  const driver = driverSimple;
  jest.setTimeout(100000); // allow time for all these tests to run


    function makeIDFromLink(link:string){
      return link.replace("https",'').replace("http",'');
    }
  
    async function getIndexData(className: string){
      const result: {
        text: string,
        link: string,
        linkForID: string,
        className: string,
      }[] = [];
      console.log(`process ${className}`);
      const x = await driver.findElements(
        webdriver.By.className(className)
      );
      // console.log(`found ${x.length} textwidgets`);
      if(x.length === 1){
        // console.log(`look for children`);
        const children = await x[0].findElements(
          webdriver.By.xpath("./child::*")
        );
       // console.log(`got ${children.length} children`);
        for(let j = 0; j < children.length; j = j + 1){
          const txt = await children[j].getText();
          if(txt === ''){
            continue;
          }
          // console.log(`text is ${txt}`);
          const link = await children[j].getAttribute("href");
          // console.log(`here's the link ${link}`);
          result.push({
            text: txt,
            link: link,
            linkForID: makeIDFromLink(link),
            className: className, 
          })
        }        
      }
      return result;
    }
  
    function containsTags(title: string, tags: string[]){
      for(const tag of tags){
        if(title.includes(tag)){
          return true;
        }
      }
      return false;
    }
  
    function seemsLive(title: string){
      return containsTags(title, ["Junction", "Portland Arms", "Parker's Piece",
        "Corner House", "Rescue Rooms", "Corn Exchange",
        "Home Festival, Mundford", "Cambridge Folk Festival",
        "Thetford Forest", "Blue Moon", "Roundhouse"]); 
    }
    function seemsSingles(title: string){
      return containsTags(title, ['single', 'EP']);
    }
    function seemsAlbums(title: string){
      return containsTags(title, ['LP']);
    }
  
    function makeTextForPostDataFeedback(items: {
      postTitle: string,
      linkText: string,
      link: string,
      className: string,    
    }[]){
      let resultForFeedback = ``;
      for( const i of items){
        resultForFeedback += `{
          postTitle: \`${i.postTitle}\`,
          linkText: \`${i.linkText}\`,
          link: \`${i.link}\`,
          className: \`${i.className}\`,
        },`;
      }
      resultForFeedback += `\n}`;
      return resultForFeedback
    }
  
    function makeTextForIndexDataFeedback(items: {
      text: string,
      link: string,
      linkForID: string,
      className: string,  
    }[]){
      let resultForFeedback = ``;
      for( const i of items){
        resultForFeedback += `{
          text: \`${i.text}\`,
          link: \`${i.link}\`,
          linkForID: \`${i.linkForID}\`,
          className: \`${i.className}\`,
        },`;
      }
      resultForFeedback += `\n}`;
      return resultForFeedback
    }
  
    function makeHMTLForNewIndex(
      index: {
        text: string,
        link: string,
        className: string,
        guessed: boolean  
      }[],
      highlightGuesses: boolean,
    ){
      let result = ``;

      if(highlightGuesses){
        result += `
        <!doctype html>
        <html dir="ltr" lang="en">
          <head>
            <meta charset="utf-8">
            <title>CMR Index with highlighting</title>
            <style>
              body {
                margin: 0;
              }
            </style>
          </head>
          <body>`
      }
      result +=`
      <h2>About</h2>
      <a href="https://cambridgemusicreviews.net/about/">About this site</a>`;
  
  
      [{className: 'cmr-live', headerText: 'Live Reviews'}, 
       {className: 'cmr-albums', headerText: 'Album reviews'}, 
       {className: 'cmr-singles', headerText: 'Singles and EPs'}, 
       {className: 'cmr-extras', headerText: 'Extras'}].map((x)=>{
  
        result += `\n<p>`;
        result += `\n<h2>${x.headerText}</h2>`;
        result += `\n<div class="${x.className}">`;
        const section = index.filter((i)=>{
          return i.className === x.className;
        });
        for(const idx of section){
          if(highlightGuesses && idx.guessed){
            result += `\n<mark>`;
          }
          result += `\n<a href="${idx.link}">${idx.text}</a><br/>`;
          if(highlightGuesses && idx.guessed){
            result += `\n</mark>`;
          }
        }
        result += `\n</div>`;
      });
      if(highlightGuesses){
        result += `</body></html>`;
      }
      return result;
    }
  
    function makeTextForSort(text: string){
      let result = text;
      if(result.startsWith('The ')){
        result = result.substring(4);
      }
      if(result.startsWith('\'')){
        result = result.substring(1);
      }
      if(result.startsWith('\"')){
        result = result.substring(1);
      }
      console.log(`${result}`);
      return result;
    }
  
    it('scrape cmr data', () => {
      return new Promise<void>(async (resolve, reject) => {
  
        await driver.get(`https://cambridgemusicreviews.net/`);
    
        // const prompt = require('prompt-sync')(); 
        // const name = prompt('What is your name?');
        // console.log(`Hey there ${name}`);
  
        let currentIndexItems: {
          text: string,
          link: string,
          linkForID: string,
          className: string,
        }[] = [];      
        const className = 'cmr-live';
        currentIndexItems = currentIndexItems.concat(await getIndexData('cmr-live'));
        currentIndexItems = currentIndexItems.concat(await getIndexData('cmr-albums'));
        currentIndexItems = currentIndexItems.concat(await getIndexData('cmr-singles'));
        currentIndexItems = currentIndexItems.concat(await getIndexData('cmr-extras'));
        
        console.log(`found data for ${currentIndexItems.length} index entries`);  
  
        const fs = require('fs');
        fs.writeFile("./scraped_data/currentIndexItems.txt", makeTextForIndexDataFeedback(currentIndexItems), function(err: any) {
          if(err) { return console.log(err);}
          console.log("The file currentIndexItems.txt was saved!");
        }); 
  
        const providedIndexItems : {
          text: string,
          link: string,
          linkForID: string,
          className: string,  
        }[] = [
        ];
  
        for(const currentIndexItem of currentIndexItems){
          const match = providedIndexItems.find((item)=>{
            return item.linkForID === currentIndexItem.linkForID;
          });
          if(match !== undefined){
            currentIndexItem.className = match.className;
            currentIndexItem.text = match.text;
          }
        }
  
        let postData: {
          postTitle: string,
          link: string,
          linkForID: string,
        }[] = [];  
        for(let pageNum = 1; pageNum < 1000; pageNum = pageNum + 1){
          const url = "https://public-api.wordpress.com/rest/v1.1/sites/"
            +"cambridgemusicreviews.net/posts"
            + "?context=\"display\""
            + "&page="+pageNum;
          await driver.get(url);
          const txtElts = await driver.findElements(
            webdriver.By.xpath("//descendant::pre")
          );
          // console.log(`found ${txtElts.length} text elts`);
          if(txtElts.length === 1){
            const json = JSON.parse(await txtElts[0].getText());
            console.log(`loaded ${json.posts.length} posts`);
            if(json.posts.length === 0){
              break;
            }
            for(const post of json.posts){
              postData.push({
                postTitle: post.title.normalize(),
                link: post.URL,
                linkForID: makeIDFromLink(post.URL),
              });
            }
          }
        }
  
        const unIndexedPosts = postData.filter((post)=>{
          return currentIndexItems.find((i)=>{
            // sometimes links are http and sometimes https
            return i.linkForID === post.linkForID;
          }) === undefined;
        })
  
        console.log(`need indexing for ${unIndexedPosts.length} posts`);
        let newIndexItems: {
          postTitle: string,
          linkText: string,
          link: string,
          className: string,
          guessed: boolean,
        }[] = []; 
  
  
        const providedPostItems : {
          postTitle: string,
          linkText: string,
          link: string,
          className: string,
        }[] = [
        ]; 
  
        for(const unIndexedPost of unIndexedPosts){
          const newIndexItem = {
            postTitle: unIndexedPost.postTitle,
            linkText: unIndexedPost.postTitle,
            link: unIndexedPost.link,
            className: '',
          }
          const match = providedPostItems.find((item)=>{
            return item.link === newIndexItem.link;
          });
          if(match !== undefined){
            newIndexItem.linkText = match.linkText;
            newIndexItem.className = match.className;
            // take this as-is
            newIndexItems.push({
              ...newIndexItem,
              guessed: false,
            });
            continue;
          }
  
          if(seemsLive(unIndexedPost.postTitle)){
            newIndexItem.className = 'cmr-live';
          }
          if(seemsAlbums(unIndexedPost.postTitle)){
            newIndexItem.className = 'cmr-albums';
          }
          if(seemsSingles(unIndexedPost.postTitle)){
            newIndexItem.className = 'cmr-singles';
          }
  
          if(newIndexItem.className === 'cmr-singles' || newIndexItem.className === 'cmr-albums'){
            const n = newIndexItem.postTitle.indexOf(' : ');
            if(n > 0){
              newIndexItem.linkText = newIndexItem.postTitle.substring(0, n);
            }
          }
  
          newIndexItems.push({
            ...newIndexItem,
            guessed: true,
          });
        }
  
        console.log(`newIndexItems are ${makeTextForPostDataFeedback(newIndexItems)}`);
  
  
        for(const newIndexItem of newIndexItems){
          // does linktext match another in the same category?  May need to adjust both...
          const match = currentIndexItems.find((i)=>{
            return i.className === newIndexItem.className && i.text.startsWith(newIndexItem.linkText);
          })
          if(match !== undefined){
            match.text = match.text+` !!!!!!!!!! NEEDSFIX`;
            newIndexItem.linkText = newIndexItem.linkText+` !!!!!!!!!! NEEDSFIX`;   
          }
        }


        fs.writeFile("./scraped_data/newIndexItems.txt", makeTextForPostDataFeedback(newIndexItems), function(err: any) {
          if(err) { return console.log(err);}
          console.log("The newIndexItems.txt file was saved!");
        }); 
  
        const newIndex: {
          text: string,
          textForSorting: string
          link: string,
          className: string,
          guessed: boolean,
        }[] = currentIndexItems.map((i)=>{
          return {
            text: i.text,
            textForSorting: makeTextForSort(i.text),
            link: i.link,
            className: i.className,
            guessed: false,
          }
        }).concat(newIndexItems.map((i)=>{
          return {
            text: i.linkText,
            textForSorting: makeTextForSort(i.linkText),
            link: i.link,
            className: i.className,
            guessed: i.guessed,
          }
        }));
  
        const classNameOrder:{ [key: string]: number } = {
          'cmr-live': 0,
          'cmr-albums': 1,
          'cmr-singles': 2,
          'cmr-extras': 3,
        }
  
        newIndex.sort((a,b)=>{
          const classA:number = classNameOrder[a.className];
          const classB:number = classNameOrder[b.className];
          if(classA < classB) return -1;
          if(classA > classB) return 1;
          let textA:string = a.textForSorting;
          let textB:string = b.textForSorting;
          if(textA < textB) return -1;
          if(textA > textB) return 1;
          return 0;
        });
  
        const result = '';
  
        fs.writeFile("./scraped_data/newCmrIndexWithGuessesHighlighted.html", makeHMTLForNewIndex(newIndex, true), function(err: any) {
          if(err) { return console.log(err);}
          console.log("The file was saved!");
        }); 
        fs.writeFile("./scraped_data/newCmrIndex.html", makeHMTLForNewIndex(newIndex, false), function(err: any) {
          if(err) { return console.log(err);}
          console.log("The file was saved!");
        }); 
        resolve();
      });
    });

  afterAll(async () => {
    await driver.quit();
  });
});
