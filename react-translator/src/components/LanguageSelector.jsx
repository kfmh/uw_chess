const LANGUAGES = {
    "Acehnese (Arabic script)": "ace_Arab",
    "Acehnese (Latin script)": "ace_Latn",
    "Afrikaans": "afr_Latn",
    "English": "eng_Latn",
  }
  
  export default function LanguageSelector({ type, onChange, defaultLanguage }) {
    return (
      <div className='language-selector'>
        <label>{type}: </label>
        <select onChange={onChange} defaultValue={defaultLanguage}>
          {Object.entries(LANGUAGES).map(([key, value]) => {
            return <option key={key} value={value}>{key}</option>
          })}
        </select>
      </div>
    )
  }