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

export function useVoiceDictation({
  onTranscript,
  enabled = true,
}: UseVoiceDictationOptions): UseVoiceDictationReturn {
  const [isRecording, setIsRecording] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSupported, setIsSupported] = useState(false)
  const processorRef = useRef<AudioWorkletNode | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const recorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  useEffect(() => {
    setIsSupported(
      typeof navigator !== 'undefined' &&
        navigator.mediaDevices !== undefined &&
        typeof navigator.mediaDevices.getUserMedia === 'function',
    )
  }, [])

  const stopRecording = useCallback(() => {
    if (recorderRef.current && recorderRef.current.state !== 'inactive') {
      recorderRef.current.stop()
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    if (processorRef.current) {
      processorRef.current.disconnect()
      processorRef.current = null
    }
    setIsRecording(false)
  }, [])

  const startRecording = useCallback(async () => {
    if (!enabled || !isSupported) return

    setError(null)
    chunksRef.current = []

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
          ? 'audio/webm;codecs=opus'
          : 'audio/webm',
      })

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })

        try {
          const { AutoProcessor, AutoModelForSpeechSeq2Seq, AutoTokenizer } = await import(
            '@xenova/transformers'
          )

          const processor = await AutoProcessor.from_pretrained(
            'Xenova/whisper-tiny',
          )
          const model = await AutoModelForSpeechSeq2Seq.from_pretrained(
            'Xenova/whisper-tiny',
          )
          const tokenizer = await AutoTokenizer.from_pretrained(
            'Xenova/whisper-tiny',
          )

          const audioArrayBuffer = await blob.arrayBuffer()
          const audioContext = new AudioContext({ sampleRate: 16000 })
          const audioBuffer = await audioContext.decodeAudioData(audioArrayBuffer)
          const audioData = audioBuffer.getChannelData(0)

          const inputs = await processor(audioData, {
            sampling_rate: 16000,
            return_tensors: 'pt',
          })

          const outputs = await model.generate({
            input_features: inputs.input_features,
            max_new_tokens: 128,
          })

          const transcription = tokenizer.decode(outputs[0], { skip_special_tokens: true })

          if (typeof transcription === 'string' && transcription.trim()) {
            onTranscript(transcription.trim())
          }

          await audioContext.close()
        } catch (err) {
          console.error('Transcription error:', err)
          setError('Voice transcription failed. Try typing instead.')
        }

        stopRecording()
      }

      recorder.start()
      recorderRef.current = recorder
      setIsRecording(true)
        } catch {
          setError('Microphone access denied. Try typing instead.')
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
