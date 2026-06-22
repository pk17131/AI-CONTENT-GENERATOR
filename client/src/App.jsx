import React, {useState} from 'react'
import Editor from './components/Editor'
import Settings from './components/Settings'
import Output from './components/Output'

export default function App(){
  const [prompt, setPrompt] = useState('')
  const [tone, setTone] = useState('neutral')
  const [length, setLength] = useState('short')
  const [style, setStyle] = useState('article')
  const [assistant, setAssistant] = useState('chatgpt')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // generateContent supports options:
  // { lengthOverride: 'short'|'medium'|'long', append: boolean }
  async function generateContent(opts = {}){
    const { lengthOverride, append } = opts
    const useLength = lengthOverride || length
    setLoading(true)
    setError(null)
    if(!append) setResponse('')
    try{
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, tone, length: useLength, style, assistant })
      })
      if(!res.ok) throw new Error(await res.text())
      const data = await res.json()
      const text = data.text ?? JSON.stringify(data)
      if(append && response) setResponse(prev => prev + '\n\n' + text)
      else setResponse(text)
    }catch(e){
      setError(e.message)
    }finally{
      setLoading(false)
    }
  }

  function regenerate(){
    generateContent({ lengthOverride: length, append: false })
  }

  function expandContent(){
    const next = length === 'short' ? 'medium' : length === 'medium' ? 'long' : 'long'
    generateContent({ lengthOverride: next, append: true })
  }

  return (
    <div className="app">
      <header className="header">
        <h1>AI Content Generator</h1>
      </header>
      <main className="main">
        <section className="left">
          <Editor prompt={prompt} setPrompt={setPrompt} />
          <Settings
            tone={tone}
            setTone={setTone}
            length={length}
            setLength={setLength}
            style={style}
            setStyle={setStyle}
            assistant={assistant}
            setAssistant={setAssistant}
          />
          <div className="controls">
            <button onClick={generateContent} disabled={loading || !prompt.trim()}>
              {loading ? 'Generating...' : 'Generate'}
            </button>
            <button onClick={() => { setPrompt(''); setResponse(''); setError(null) }}>
              Reset
            </button>
          </div>
          {error && <div className="error">Error: {error}</div>}
        </section>
        <section className="right">
          <Output response={response} onRegenerate={regenerate} onExpand={expandContent} loading={loading} error={error} />
        </section>
      </main>
    </div>
  )
}
