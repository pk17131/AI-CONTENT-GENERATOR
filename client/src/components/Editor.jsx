import React from 'react'

export default function Editor({prompt, setPrompt}){
  return (
    <div className="editor">
      <label>Prompt</label>
      <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Describe what you want the AI to write..." rows={8} />
    </div>
  )
}
