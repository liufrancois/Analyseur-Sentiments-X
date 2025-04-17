import React,{ useState } from 'react';
import './App.css';

function App(){
  const [hashtag, setHashtag] = useState('');
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () =>{
    if (!hashtag.startsWith('#')){
      alert("Ajoute un # devant le mot-clé !");
      return;
    }

    setLoading(true);
    try{
      const response = await fetch('http://localhost:5000/search',{
        method: 'POST',
        headers:{ 'Content-Type': 'application/json' },
        body: JSON.stringify({ hashtag })
      });

      const data = await response.json();

      if (data.tweets){
        setTweets(data.tweets);
      } else if (data.error){
        alert("Erreur API : " + data.error);
      } else{
        alert("Erreur inconnue.");
      }

    } catch (error){
      alert("Erreur de connexion avec le serveur.");
      console.error(error);
    } finally{
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Analyse de Tweets</h1>

      <input
        type="text"
        value={hashtag}
        onChange={(e) => setHashtag(e.target.value)}
        placeholder="#exemple"
      />
      <button onClick={handleSearch}>Rechercher</button>

     {loading && <p>Chargement...</p>}

      <div className="tweets">
       {tweets.map((tweet, index) => (
          <div key={index} className="tweet">
            <p>{tweet.mentions && tweet.mentions.length > 0 ? tweet.mentions.map(m => `@${m}`).join(' ') : ''}</p>
            <p>{tweet.text}</p>
            <p>{tweet.hashtags && tweet.hashtags.length > 0 ? tweet.hashtags.map(h => `#${h}`).join(' ') : ''}</p>
            <p className={`sentiment ${tweet.sentiment}`}>{tweet.sentiment}</p>
          </div>
        ))}
      </div>

    </div>
  );
}

export default App;
