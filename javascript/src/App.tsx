import { Component } from 'react';
import './App.css';

function App() {
  return (
    <AppContent
    >
    </AppContent>
  );
}

export default App;

interface AppState {
}
interface AppProps {
}

export class AppContent extends Component<AppProps, AppState> { 
  public constructor(props: AppProps) {
    super(props);
    this.state = {
    }
  }
  


public render() {
  return (
<>
<h2>Instructions</h2> 
npm test
<br></br>
See cambridge music reviews site come up.  See a sequence of pages displaying json come up.
<br></br>
Find files in the scraped_data folder.
<br></br>
Look at newCmrIndexWithGuessesHighlighted.html.  Find items in yellow.

<br></br>
Copy the contents of scraped_data/currentIndexItems.txt into providedIndexItems = [], in App.test.tsx.
<br></br>
Copy the contents of scraped_data/newIndexItems.txt into providedPostItems = [], in App.test.tsx.
<br></br>
Edit providedPostItems data so that the link text looks good to see in the index, and items are in the right category.
<br></br>
Edit providedPostItems and providedIndexItems data so that the link texts looks good to see in the index.
<br></br>
Keep doing npm test and reviewing the index.  When happy, copy newCmrIndex.html into the WordPress widget, review and publish.
</>
    );
  }
}
