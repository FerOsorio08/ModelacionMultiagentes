using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasicLerp : MonoBehaviour
{
    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 endPos;
    [Range(0.0f, 1.0f)]
    [SerializeField] float t;

    [SerializeField] float moveTime;
    float elapsedTime = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        t = elapsedTime / moveTime;
        Vector3 position = startPos + (endPos - startPos) * t;
        transform.position = position;
        elapsedTime += Time.deltaTime;
        if (elapsedTime > moveTime)
        {
            elapsedTime = 0.0f;
        }


    }
}
