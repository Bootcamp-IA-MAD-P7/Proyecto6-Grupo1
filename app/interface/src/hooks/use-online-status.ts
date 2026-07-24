import { useCallback, useEffect, useState } from 'react'

export type ConnectivityCheck = () => Promise<boolean>

export const checkServiceConnectivity: ConnectivityCheck = async () => {
  if (!navigator.onLine) return false

  try {
    const response = await fetch('/connectivity-check.txt', {
      method: 'HEAD',
      cache: 'no-store',
      credentials: 'same-origin',
    })
    return response.ok
  } catch {
    return false
  }
}

export function useOnlineStatus(connectivityCheck: ConnectivityCheck = checkServiceConnectivity) {
  const [isOnline, setIsOnline] = useState(() => navigator.onLine)

  const verifyOnline = useCallback(async () => {
    const online = await connectivityCheck()
    setIsOnline(online)
    return online
  }, [connectivityCheck])

  useEffect(() => {
    const updateStatus = () => {
      if (!navigator.onLine) {
        setIsOnline(false)
        return
      }

      void verifyOnline()
    }

    window.addEventListener('online', updateStatus)
    window.addEventListener('offline', updateStatus)
    void verifyOnline()

    return () => {
      window.removeEventListener('online', updateStatus)
      window.removeEventListener('offline', updateStatus)
    }
  }, [verifyOnline])

  return { isOnline, verifyOnline }
}
