import React from 'react'

export default function Output({response, onRegenerate, onExpand, loading, error}){
  function download(){
    const blob = new Blob([response || ''], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'ai-output.txt'
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  if(error) return (
    <div className="output error">
      <div className="output-actions">
        <button onClick={onRegenerate} disabled={loading}>Retry</button>
      </div>
      <div>Error: {error}</div>
    </div>
  )

  if(!response) return (
    <div className="output empty">
      <strong>No output yet.</strong>
      <div className="hint">Try entering a clear prompt and click Generate. Examples:</div>
      <ul>
        <li>Create a short blog intro about remote work benefits.</li>
        <li>Summarize the following text into 3 bullets: ...</li>
        <li>Write a catchy social post about launching a product.</li>
      </ul>
      <div className="output-actions">
        <button onClick={() => navigator.clipboard.writeText('Write a short article about X')}>Copy Example</button>
      </div>
    </div>
  )

  return (
    <div className="output">
      <div className="output-actions">
        <button onClick={() => navigator.clipboard.writeText(response)}>Copy</button>
        <button onClick={download}>Download</button>
        <button onClick={onRegenerate} disabled={loading}>Regenerate</button>
        <button onClick={onExpand} disabled={loading}>Expand</button>
      </div>
      <pre>{response}</pre>
    </div>
  )
}
