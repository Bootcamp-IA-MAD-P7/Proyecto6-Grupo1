import { useState, useEffect, useRef, useCallback } from 'react'

interface UseVoiceDictationOptions {
  onTranscript: (text: string) => void
  enabled?: boolean
}

interface UseVoiceDictationReturn {
  isRecording: boolean
  isSupported: boolean
  startRecording: () => void
  stopRecording: () => void
  error: string | null
}

interface SpeechRecognitionAlternativeLike {
  transcript: string
}

interface SpeechRecognitionResultLike {
  readonly [index: number]: SpeechRecognitionAlternativeLike | undefined
}

interface SpeechRecognitionResultListLike {
  readonly [index: number]: SpeechRecognitionResultLike | undefined
}

interface SpeechRecognitionEventLike extends Event {
  results: SpeechRecognitionResultListLike
  resultIndex: number
}

interface SpeechRecognitionErrorEventLike extends Event {
  error: string
  message: string
}

interface SpeechRecognitionLike {
  lang: string
  continuous: boolean
  interimResults: boolean
  maxAlternatives: number
  onresult: ((event: SpeechRecognitionEventLike) => void) | null
  onerror: ((event: SpeechRecognitionErrorEventLike) => void) | null
  onend: (() => void) | null
  start: () => void
  stop: () => void
}

type SpeechRecognitionConstructor = new () => SpeechRecognitionLike

type SpeechRecognitionWindow = Window & {
  SpeechRecognition?: SpeechRecognitionConstructor
  webkitSpeechRecognition?: SpeechRecognitionConstructor
}

const getSpeechRecognitionAPI = (): SpeechRecognitionConstructor | null => {
  if (typeof window === 'undefined') return null

  const speechWindow = window as SpeechRecognitionWindow
  return speechWindow.SpeechRecognition ?? speechWindow.webkitSpeechRecognition ?? null
}

const getRecognitionLanguage = () => document.documentElement.lang || navigator.language || 'en-US'

export function useVoiceDictation({
  onTranscript,
  enabled = true,
}: UseVoiceDictationOptions): UseVoiceDictationReturn {
  const [isRecording, setIsRecording] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSupported, setIsSupported] = useState(() => getSpeechRecognitionAPI() !== null)
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null)

  useEffect(() => {
    setIsSupported(getSpeechRecognitionAPI() !== null)
  }, [])

  const stopRecording = useCallback(() => {
    const recognition = recognitionRef.current
    recognitionRef.current = null
    recognition?.stop()
    setIsRecording(false)
  }, [])

  const startRecording = useCallback(() => {
    const SpeechRecognitionAPI = getSpeechRecognitionAPI()

    if (!enabled || !SpeechRecognitionAPI) {
      setIsSupported(false)
      return
    }

    setIsSupported(true)
    setError(null)
    stopRecording()

    const recognition = new SpeechRecognitionAPI()
    recognition.lang = getRecognitionLanguage()
    recognition.continuous = true
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onresult = (event: SpeechRecognitionEventLike) => {
      const result = event.results[event.resultIndex]
      if (result && result[0]) {
        const transcript = result[0].transcript
        if (transcript.trim()) {
          onTranscript(transcript.trim())
        }
      }
    }

    recognition.onerror = (event: SpeechRecognitionErrorEventLike) => {
      if (event.error !== 'aborted') {
        setError(
          event.error === 'not-allowed' || event.error === 'service-not-allowed'
            ? 'Microphone access was not granted. Continue by typing.'
            : 'Voice transcription failed. Continue by typing.',
        )
      }
      setIsRecording(false)
    }

    recognition.onend = () => {
      if (recognitionRef.current === recognition) {
        recognitionRef.current = null
        setIsRecording(false)
      }
    }

    recognitionRef.current = recognition

    try {
      recognition.start()
      setIsRecording(true)
    } catch {
      recognitionRef.current = null
      setError('Could not start voice recognition. Try typing instead.')
      setIsRecording(false)
    }
  }, [enabled, onTranscript, stopRecording])

  useEffect(() => {
    return () => {
      stopRecording()
    }
  }, [stopRecording])

  return {
    isRecording,
    isSupported,
    startRecording,
    stopRecording,
    error,
  }
}
