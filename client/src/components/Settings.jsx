import React from 'react'

export default function Settings({tone, setTone, length, setLength, style, setStyle, assistant, setAssistant}){
  return (
    <div className="settings">
      <div>
        <label>Tone</label>
        <select value={tone} onChange={e => setTone(e.target.value)}>
          <option value="neutral">Neutral</option>
          <option value="formal">Formal</option>
          <option value="casual">Casual</option>
          <option value="marketing">Marketing</option>
        </select>
      </div>
      <div>
        <label>Length</label>
        <select value={length} onChange={e => setLength(e.target.value)}>
          <option value="short">Short</option>
          <option value="medium">Medium</option>
          <option value="long">Long</option>
        </select>
      </div>
      <div>
        <label>Style</label>
        <select value={style} onChange={e => setStyle(e.target.value)}>
          <option value="article">Article</option>
          <option value="summary">Summary</option>
          <option value="social">Social Post</option>
          <option value="headline">Headline</option>
        </select>
      </div>
      <div>
        <label>Assistant</label>
        <select value={assistant} onChange={e => setAssistant(e.target.value)}>
          <option value="chatgpt">ChatGPT-like</option>
          <option value="gemini">Gemini-like</option>
          <option value="assistant">Assistant-style</option>
        </select>
      </div>
    </div>
  )
}
