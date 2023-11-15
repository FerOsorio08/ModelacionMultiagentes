using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasicLerp : MonoBehaviour
{
    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 finalPos;
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
        t = t * t * (3.0f - 2.0f * t);
        Vector3 position = startPos + (finalPos - startPos) * t;
        transform.position = position;
        Matrix4x4 move = HW_Transforms.TranslationMat(position.x, position.y, position.z);
        elapsedTime += Time.deltaTime;
        if (elapsedTime > moveTime)
        {
            elapsedTime = 0.0f;

            Vector3 temp = finalPos;
            finalPos = startPos;
            startPos = temp;
        }


    }
}
