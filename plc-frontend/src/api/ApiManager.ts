import { IEffectOptions } from '../domainData/DomainData';

const HOST = `http://${window.location.hostname}:8080`

const handleErrors = (res: Response) => {
    if (!res.ok) {
        throw new Error(res.statusText)
    }
}

export const setEffect = async (effectData: IEffectOptions) => {
    const res = await fetch(`${HOST}/effect/${effectData.effect}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        mode: "cors",
        // body:JSON.stringify(
            
        // )
    })
    handleErrors(res)
    return res.json()
}

export const getAvailable = async (): Promise<string[]> => {
    const res = await fetch(`${HOST}/effect/available`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        mode: "cors"
    })
    handleErrors(res)
    return await res.json()
}

export const getStatus = async (): Promise<IEffectOptions> => {
    const res = await fetch(`${HOST}/effect/current`, {
        method: "GET",
        mode: "cors"
    })
    handleErrors(res)
    return await res.json()
}

export const getOptionParameters = async (effect:string) => {
    const res = await fetch(`${HOST}/effect/${effect}/options`, {
        method: "GET",
        mode: "cors"
    })
    handleErrors(res)
    return await res.json()
}