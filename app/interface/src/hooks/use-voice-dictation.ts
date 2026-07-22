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

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList
  resultIndex: number
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string
  message: string
}

const SpeechRecognitionAPI =
  typeof window !== 'undefined'
    ? // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    : null

export function useVoiceDictation({
  onTranscript,
  enabled = true,
}: UseVoiceDictationOptions): UseVoiceDictationReturn {
  const [isRecording, setIsRecording] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSupported, setIsSupported] = useState(false)
  const recognitionRef = useRef<InstanceType<typeof SpeechRecognitionAPI> | null>(null)

  useEffect(() => {
    setIsSupported(SpeechRecognitionAPI != null)
  }, [])

  const stopRecording = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
      recognitionRef.current = null
    }
    setIsRecording(false)
  }, [])

  const startRecording = useCallback(() => {
    if (!enabled || !isSupported || !SpeechRecognitionAPI) return

    setError(null)
    stopRecording()

    const recognition = new SpeechRecognitionAPI()
    recognition.lang = 'es-ES'
    recognition.continuous = true
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const result = event.results[0]
      if (result && result[0]) {
        const transcript = result[0].transcript
        if (transcript.trim()) {
          onTranscript(transcript.trim())
        }
      }
    }

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      if (event.error !== 'aborted') {
        console.error('Speech recognition error:', event.error, event.message)
        setError('Voice transcription failed. Try typing instead.')
      }
      setIsRecording(false)
    }

    recognition.onend = () => {
      setIsRecording(false)
      recognitionRef.current = null
    }

    try {
      recognition.start()
      recognitionRef.current = recognition
      setIsRecording(true)
    } catch {
      setError('Could not start voice recognition. Try typing instead.')
      setIsRecording(false)
    }
  }, [enabled, isSupported, onTranscript, stopRecording])

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
