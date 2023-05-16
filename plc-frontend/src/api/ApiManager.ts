import { IEffectData } from '../domainData/DomainData';

// const HOST = "http://127.0.0.1:8080"
const HOST = `http://${window.location.hostname}:8080`

const handleErrors = (res: Response) => {
    if (!res.ok) {
        throw new Error(res.statusText)
    }
}

export const setEffect = async (effectData: IEffectData) => {
    const res = await fetch(`${HOST}/effect/${effectData.effect}/${effectData.brightness}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        mode: "cors"
    })
    handleErrors(res)
    return res.json()
}

export const getStatus = async () => {
    const res = await fetch(`${HOST}/effect/current`, {
        method: "GET",
        mode: "cors"
    })
    handleErrors(res)
    return res.json()
}